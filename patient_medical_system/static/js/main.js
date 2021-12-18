function change_total_fees() {
    total_fees = document.querySelector("#total-fees")
    var fees = document.getElementsByClassName("fees");
    sum = 0
    for (var i = 0; i < fees.length; i++) {
        sum += parseFloat(fees[i].value);
    }
    total_fees.value = sum
}

function searchTable(table_id) {
    var search, filter, table, tr, td, i, txtValue, found;
    search = document.getElementById("search");
    filter = search.value.toUpperCase();
    table = document.getElementById(table_id);
    tr = table.getElementsByTagName("tr");
    console.log(tr.length)
    for (i = 1; i < tr.length; i++) {
        tds = tr[i].getElementsByTagName("td");
        console.log(tds.length)
        found = false

        for (j = 0; j < tds.length; j++) {
            td = tds[j]
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    console.log(txtValue)
                    tr[i].style.display = "";   
                    found = true
                }
            }

        }
        if (!found) {
            tr[i].style.display = "none";
        }
    }
}