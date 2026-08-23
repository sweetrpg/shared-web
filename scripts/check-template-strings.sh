#!/usr/bin/env bash
# Fails the build if a template contains literal user-facing text that isn't
# wrapped in a gettext call (`{{ _('...') }}` / `{% trans %}`). See the
# `web-frontend-localization` spec (sweetrpg/platform,
# openspec/changes/full-localization-web-apps) for the convention.
#
# Allowed literals: brand/proper nouns and non-translatable strings.
set -euo pipefail
cd "$(dirname "$0")/.."

ALLOWED='SweetRPG|GitHub|Pilgrimage Software'
status=0

for template in $(find src -name '*.html'); do
    # Strip scripts, styles, HTML/Jinja comments, Jinja blocks/expressions, then
    # report remaining text between tags that isn't whitespace or bare entities.
    violations=$(
        perl -0777 -pe 's/<script.*?<\/script>//gs; s/<style.*?<\/style>//gs; s/<!--.*?-->//gs; s/{#.*?#}//gs; s/\{%.*?%\}//gs; s/\{\{.*?\}\}//gs' "$template" |
            perl -0777 -ne 'while (/>[^<]+</g) { my $t = $&; $t =~ s/^>|<$//g; my $u = $t; $u =~ s/^\s+|\s+$//g; print "$u\n" if $u =~ /\S/ && $u !~ /^(&[a-z]+;|[[:punct:]\s])*$/; }' |
            grep -vE "(${ALLOWED})" || true
    )
    if [ -n "$violations" ]; then
        echo "ERROR: $template contains hardcoded user-facing strings:"
        echo "$violations"
        status=1
    fi
done

exit $status
