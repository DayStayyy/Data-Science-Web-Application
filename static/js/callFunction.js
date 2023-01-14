var result = document.getElementById("result");

var array_of_functions_name = [
  "best_selling_products",
  "most_returned_products",
  "best_customers",
  "most_returned_customers",
  "best_selling_categories",
  "similar_products_countries",
];

async function get_data(number, function_name) {
  var data = await fetch("/api/" + function_name + "?" + "number=" + number)
    .then((response) => {
      return response.json();
    })
    .then((jsondata) => {
      return jsondata;
    });
  return data;
}

function display_table(data, first_column_name, second_column_name) {
  // clear result div
  result.innerHTML = "";
  var table = document.createElement("responsive-table");
  var tr = document.createElement("table-row");
  var th = document.createElement("table-header");
  th.appendChild(document.createTextNode(first_column_name));
  tr.appendChild(th);
  th = document.createElement("table-header");
  th.appendChild(document.createTextNode(second_column_name));
  tr.appendChild(th);
  table.appendChild(tr);
  for (const [i, val] of Object.entries(data)) {
    var tr = document.createElement("table-row");
    var td = document.createElement("td");
    td.appendChild(document.createTextNode(i));
    td.addclassName = "col col-1";
    tr.appendChild(td);
    td = document.createElement("td");
    td.appendChild(document.createTextNode(Math.abs(val)));
    tr.appendChild(td);
    table.appendChild(tr);
    td.addclassName = "col col-2";
  }
  result.appendChild(table);
}

async function call_function(number, function_name) {
  first_column_name = "";
  second_column_name = "";
  switch (function_name) {
    case "best_selling_products":
      first_column_name = "Product Name";
      second_column_name = "Number of sales";
      break;
    case "most_returned_products":
      first_column_name = "Product Name";
      second_column_name = "Number of returns";
      break;
    case "best_customers":
      first_column_name = "Customer Name";
      second_column_name = "Number of sales";
      break;
    case "most_returned_customers":
      first_column_name = "Customer Name";
      second_column_name = "Number of returns";
      break;
    case "best_selling_categories":
      first_column_name = "Category Name";
      second_column_name = "Number of sales";
      break;
    case "similar_products_countries":
      first_column_name = "Country Name";
      second_column_name = "Number of sales";
      break;
    default:
      break;
  }
  var data = await get_data(number, function_name);
  display_table(data, first_column_name, second_column_name);
}

// create button avec un menu déroulant pour choisir la fonction à appeler (best_selling_products, best_customers, etc.) et un champ pour entrer le nombre de résultats à afficher
function create_button() {
  var button = document.createElement("button");
  button.appendChild(document.createTextNode("Call function"));
  button.onclick = function () {
    var function_name = document.getElementById("function_name").value;
    var number = document.getElementById("number").value;
    call_function(number, function_name);
  };
  document.body.appendChild(button);
}

create_button();

// create input for number
function create_input_number() {
  var input = document.createElement("input");
  input.type = "text";
  input.id = "number";
  input.placeholder = "number";
  document.body.appendChild(input);
}

create_input_number();

// create select for function name
function create_select_function_name() {
  var select = document.createElement("select");
  select.id = "function_name";
  for (var i = 0; i < array_of_functions_name.length; i++) {
    var option = document.createElement("option");
    option.value = array_of_functions_name[i];
    option.text = array_of_functions_name[i];
    select.appendChild(option);
  }
  document.body.appendChild(select);
}

create_select_function_name();
call_function(10, "best_selling_products");
