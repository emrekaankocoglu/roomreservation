$(document).ready(function() {
    $('#dateForm').submit(function(event) {
        event.preventDefault();
        const formData = $(this).serialize();
        const ws = new WebSocket("ws://" + location.hostname + ":8001");
        ws.onopen = function() {
            const payload = {
                message: "REQUEST", 
                data: {command: "roomView", start: $("#start").val(), end: $("#end").val()},
                auth: {username: user, token: token}}
            ws.send(JSON.stringify(payload));
        };
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.message == "ERROR") {
                alert(data.data.message);
            }
            else {
                renderRoomView(data.data);
            }
        }

    });
});

function renderRoomView(data) {
    // Clear tabs
    $('#tabs').empty();
    if ($('#tabs').hasClass('ui-tabs')) {
        $('#tabs').tabs("destroy");
    }
    jsonData = data.response;
    var tabsHtml = '';
        for (var key in jsonData) {
            if (jsonData.hasOwnProperty(key)) {
                tabsHtml += '<li><a href="#' + key + '">' + key + '</a></li>';
            }
        }

        $('#tabs').append('<ul>' + tabsHtml + '</ul>');

        // Create tab content for each key
        for (var key in jsonData) {
            var table = `
            <table class="table table-striped table-bordered table-hover">
            <thead>
            <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Description</th>
                <th>Category</th>
                <th>Capacity</th>
                <th>Duration</th>
                <th>Start Time</th>
                <th>Weekly</th>
                <th>Location</th>
            </tr>
            </thead>
            <tbody id="${key}">

            

            `;
            jsonData[key].forEach(function(row) {
                console.log(row[0]);
                console.log($('#' + key));
                const rowHtml = `
                    <tr>
                        <td>${row[0].id}</td>
                        <td>${row[0].title}</td>
                        <td>${row[0].description}</td>
                        <td>${row[0].category}</td>
                        <td>${row[0].capacity}</td>
                        <td>${row[0].duration}</td>
                        <td>${row[0].start_time}</td>
                        <td>${row[0].weekly}</td>
                        <td>${row[0].location}</td>
                    </tr>`;

                    table += rowHtml;
                });
            table+='</tbody></table>';
            $('#tabs').append('<div id="' + key + '" class="tab-content">' +table+ '</div>');
        }

        // Initialize jQuery UI tabs
        $('#tabs').tabs();
};
    


