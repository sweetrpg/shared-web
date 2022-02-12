$(document).ready(function () {
    // $('div.col.volume').each(function (i, e) {
    //     var id = e.id;
    //     // var created = $(e).find("time#volume-" + id + "-created").attr("datetime");
    //     var updated = $(e).find("time#volume-" + id + "-updated").attr("datetime");
    //     // var createdBy = $(e).find("data#volume-" + id + "-created-by").attr("value");
    //     // var updatedBy = $(e).find("data#volume-" + id + "-updated-by").attr("value");
    //     var cell = $(e).find("#volume-" + id + "-date-info");
    //     $(cell).html(moment(updated).fromNow());
    // });
});

var start = 0;
var length = 20;

function fetch_volumes(start, length) {
    var api_url = $('data#api-base-url').val();
    fetch(api_url + '/volumes/data?start=' + start + '&length=' + length)
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            vue.volumes = data.items;
        });
}

let vue = Vue({
    el: '#app',
    data: {
        'volumes': []
    },
    created() {
        fetch_volumes(start, length);
    }
});
