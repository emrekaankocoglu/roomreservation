$(document).ready(function() {
    $('#dateForm').submit(function(event) {
        event.preventDefault();
        const formData = $(this).serialize();
        const ws = new WebSocket("ws://" + location.hostname + ":8001");
        ws.onopen = function() {
            const payload = {
                message: "REQUEST", 
                data: {command: "dayView", start: $("#start").val(), end: $("#end").val()},
                auth: {username: user, token: token}}
            ws.send(JSON.stringify(payload));
        };
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.message == "ERROR") {
                alert(data.data.message);
            }
            else {
                renderDayView(data.data);
            }
        }

    });
});

function renderDayView(data) {
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
                <th>Room Name</th>
                <th>Room Capacity</th>
                <th>Room Location</th>
                <th>Room Working Hours</th>
            </tr>
            </thead>
            <tbody id="${key}">

            

            `;
            var svg =`<svg height="200" width="200">
            <defs>
            <pattern id="smallGrid" width="8" height="8" patternUnits="userSpaceOnUse">
              <path d="M 8 0 L 0 0 0 8" fill="none" stroke="gray" stroke-width="0.5"/>
            </pattern>
            <pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse">
              <rect width="80" height="80" fill="url(#smallGrid)"/>
              <path d="M 80 0 L 0 0 0 80" fill="none" stroke="gray" stroke-width="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />`
            jsonData[key].forEach(function(row) {
                console.log(row);
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
                        <td>${row[1].name}</td>
                        <td>${row[1].capacity}</td>
                        <td>${row[1].x + "," + row[1].y}</td>
                        <td>${row[1].workinghours}</td>

                    </tr>`;

                    table += rowHtml;
                const svgHtml = `
                <text x="${row[1].x}" y="${row[1].y}" font-size="10px">${row[0].title}</text>
                <circle cx="${row[1].x}" cy="${row[1].y}" r="5" fill="green" />
                `
                svg += svgHtml;
                });
            table+='</tbody></table>';
            svg+='</svg>';
            $('#tabs').append('<div id="' + key + '" class="tab-content">' +table+ svg + '</div>');
        }

        // Initialize jQuery UI tabs
        $('#tabs').tabs();
};
    


