$(document).ready(function () {
    $('div.col.volume').each(function (e) {
        var id = e.id;
        // var created = $(e).find("time#volume-" + id + "-created").attr("datetime");
        var updated = $(e).find("time#volume-" + id + "-updated").attr("datetime");
        // var createdBy = $(e).find("data#volume-" + id + "-created-by").attr("value");
        // var updatedBy = $(e).find("data#volume-" + id + "-updated-by").attr("value");
        var cell = $(e).find("#volume-" + id + "-date-info");
        $(cell).html(moment(updated).fromNow());
    });
});
