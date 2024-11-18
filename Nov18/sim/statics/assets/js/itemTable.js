
// Initialize DataTable with JSON data from API ================================================
$(document).ready(function() {
    const table = new DataTable('#daTable', {
      "ajax": {
        "url": "/items",  // Fetch data from /items endpoint
        "dataSrc": ""     // Use a flat array directly
      },
      "columns": [
        {
          "className": 'dt-control',
          "orderable": false,
          "data": null,
          "defaultContent": ''
        },
        { "data": "id" },
        { "data": "serial_number" },
        { "data": "description" },
        { "data": "location" },
        { "data": "itypes" },
        { "data": "brand" },
        { "data": "model" }
      ],
      paging: false,
      scrollCollapse: true,
      scrollY: '400px',
      order: [[1, 'asc']]
    });

    // Array to track the ids of the details displayed rows
    const detailRows = [];

    // Add event listener for clicking on the child row control
    $('#daTable tbody').on('click', 'td.dt-control', function () {
      const tr = $(this).closest('tr');
      const row = table.row(tr);
      const idx = detailRows.indexOf(tr[0].id);

      if (row.child.isShown()) {
        tr.removeClass('details');
        row.child.hide();

        // Remove from the 'open' array
        detailRows.splice(idx, 1);
      }
      else {
        tr.addClass('details');
        row.child(format(row.data())).show();

        // Add to the 'open' array
        if (idx === -1) {
          detailRows.push(tr[0].id);
        }
      }
    });

    // On each draw, loop over the detailRows array and show any child rows
    table.on('draw', () => {
      detailRows.forEach((id, i) => {
        const el = document.querySelector(`#${id} td.dt-control`);
        if (el) {
          el.dispatchEvent(new Event('click', { bubbles: true }));
        }
      });
    });
  });

function format(d) {
return (
  '<div class="container" style="background-color:beige ">' +
  '<table class="table table-bordered" style="width: 70%; margin: auto; font-size: 0.875rem;">' + // Smaller table width and font size
  '<thead>' +
    '<tr style="background-color: #800000; color: white;">' + // Header color styling
      '<th>Actions</th>' +
      '<th>Status</th>' +
      '<th>MAC Address</th>' +
      '<th>Remarks</th>' +
      '<th>Switch</th>' +
      '<th>Timestamp</th>' +
    '</tr>' +
  '</thead>' +
  '<tbody>' +
    '<tr>' +
      '<td>' +
        '<div style="display: flex; gap: 15px;">' +
          
          '<i class="bi bi-file-earmark-plus icon-large" style="font-size: 1.2rem; margin-right: 18px;" '+
          'onclick="openModal(null, \'new\')" data-bs-toggle="tooltip" title="Create New"></i>' +

          '<i class="bi bi-pencil-square icon-large" style="font-size: 1.2rem; margin-right: 18px;" '+
          'onclick="openModal(' + d.id + ', \'modify\')" data-bs-toggle="tooltip" title="Modify"></i>' +

          '<i class="bi bi-copy   icon-large" style="font-size: 1.2rem; margin-right: 18px;" '+
          'onclick="openModal(' + d.id + ', \'clone\')"  data-bs-toggle="tooltip" title="Clone"></i>' +
          
          '<i class="bi bi-trash3 icon-large" style="font-size: 1.2rem; margin-right: 18px;" '+
          'onclick="openDelModal(' + d.id + ', \'delete\')" data-bs-toggle="tooltip" title="Delete"></button> </i> ' +

        '</div>' +
      '</td>' +
      '<td>' + d.status + '</td>' +
      '<td>' + (d.macadd ? d.macadd : 'N/A') + '</td>' +
      '<td>' + (d.remarks ? d.remarks : 'N/A') + '</td>' +
      '<td>' + d.switch + '</td>' +
      '<td>' + d.timestamp + '</td>' +
    '</tr>' +
    '</tbody>' +
    '</table>' +
  '</div>'
);
}
