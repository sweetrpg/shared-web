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

function fetch_persons(start, length) {
    var api_url = $('data#api-base-url').val();
    fetch(api_url + '/persons/data?start=' + start + '&length=' + length)
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            vue.persons = data.items;
        });
}

let vue = Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        'persons': [],
        'startPage': 0,
        'pageLength': 20,
    },
    created() {
        fetch_persons(this.startPage, this.pageLength);
    }
});
