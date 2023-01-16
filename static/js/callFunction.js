var array_of_functions_name = [
  "best_selling_products",
  "most_returned_products",
  "best_customers",
  "most_returned_customers",
];

var array_of_functions_name_modelisation = [
  "plot_top_product",
  "plot_top_products_by_country",
  "plot_top_customers",
  "plot_top_returned_products",
];

async function get_data(number, function_name) {
  console.log("get_data" + number, " ", function_name);
  var data = await fetch("/api/" + function_name + "?" + "number=" + number)
    .then((response) => {
      return response.json();
    })
    .then((jsondata) => {
      return jsondata;
    });
  console.log(data);
  return data;
}

function display_table(data, first_column_name, second_column_name, table_id) {
  // clear result div
  var table = document.getElementById(table_id);
  table.innerHTML = "";
  var tr = document.createElement("tr");
  var th = document.createElement("th");
  th.appendChild(document.createTextNode(first_column_name));
  tr.appendChild(th);
  th = document.createElement("th");
  th.appendChild(document.createTextNode(second_column_name));
  tr.appendChild(th);
  table.appendChild(tr);
  for (const [i, val] of Object.entries(data)) {
    var tr = document.createElement("tr");
    var td = document.createElement("td");
    td.appendChild(document.createTextNode(i));
    tr.appendChild(td);
    td = document.createElement("td");
    if (table_id == "result_variation") {
      td.appendChild(document.createTextNode(parseInt(val) + "%"));
    } else {
      td.appendChild(document.createTextNode(val));
    }
    tr.appendChild(td);
    table.appendChild(tr);
  }
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
  display_table(data, first_column_name, second_column_name, "result");
}

// create button avec un menu déroulant pour choisir la fonction à appeler (best_selling_products, best_customers, etc.) et un champ pour entrer le nombre de résultats à afficher
function create_button(div) {
  var button = document.createElement("button");
  button.appendChild(document.createTextNode("Call"));
  button.onclick = function () {
    var function_name = document.getElementById("function_name").value;
    var number = document.getElementById("number").value;
    call_function(number, function_name);
  };
  div.appendChild(button);
}

// create input for number
function create_input_number(div) {
  var input = document.createElement("input");
  input.type = "text";
  input.id = "number";
  input.value = 10;
  input.placeholder = "number of results";
  div.appendChild(input);
}

// create select for function name
function create_select_function_name(div) {
  var select = document.createElement("select");
  select.id = "function_name";
  for (var i = 0; i < array_of_functions_name.length; i++) {
    var option = document.createElement("option");
    option.value = array_of_functions_name[i];
    option.text = array_of_functions_name[i];
    select.appendChild(option);
  }
  div.appendChild(select);
}

function create_function_selectors() {
  var main = document.getElementById("main");
  var div = document.createElement("div");
  div.className = "function_selectors";
  create_select_function_name(div);
  create_input_number(div);
  create_button(div);

  main.appendChild(div);
}

create_function_selectors();

function create_result_table() {
  var div = document.createElement("div");
  div.className = "table-wrapper";
  var table = document.createElement("table");
  table.id = "result";
  table.className = "fl-table";
  div.appendChild(table);
  // get right div
  var main = document.getElementById("main");
  main.appendChild(div);
}

create_result_table();

call_function(10, "best_selling_products");

// call /api/product_with_biggest_variation, the argument is start_date, end_date, start_date2, end_date2, number, ascending
async function get_data_product_with_biggest_variation(
  start_date,
  end_date,
  start_date2,
  end_date2,
  number,
  ascending
) {
  var data = await fetch(
    "/api/product_with_biggest_variation?" +
      "start_date=" +
      start_date +
      "&end_date=" +
      end_date +
      "&start_date2=" +
      start_date2 +
      "&end_date2=" +
      end_date2 +
      "&number=" +
      number +
      "&ascending=" +
      ascending
  )
    .then((response) => {
      return response.json();
    })
    .then((jsondata) => {
      return jsondata;
    });
  console.log(data);
  return data;
}

async function call_function_product_with_biggest_variation(
  start_date,
  end_date,
  start_date2,
  end_date2,
  number,
  ascending
) {
  var data = await get_data_product_with_biggest_variation(
    start_date,
    end_date,
    start_date2,
    end_date2,
    number,
    ascending
  );
  display_table(
    data,
    "Product Name",
    "Variation in pourcent",
    "result_variation"
  );
}

// create button avec un menu déroulant pour choisir la fonction à appeler (best_selling_products, best_customers, etc.) et un champ pour entrer le nombre de résultats à afficher
function create_button_product_with_biggest_variation(div) {
  var button = document.createElement("button");
  button.appendChild(document.createTextNode("Call"));
  button.onclick = function () {
    var start_date = document.getElementById("start_date").value;
    var end_date = document.getElementById("end_date").value;
    var start_date2 = document.getElementById("start_date2").value;
    var end_date2 = document.getElementById("end_date2").value;
    var number = document.getElementById("number_variation").value;
    var ascending = document.getElementById("ascending").value;
    call_function_product_with_biggest_variation(
      start_date,
      end_date,
      start_date2,
      end_date2,
      number,
      ascending
    );
  };
  div.appendChild(button);
}

// create input for number
function create_input_number_product_with_biggest_variation(div) {
  var input = document.createElement("input");
  input.type = "text";
  input.id = "number_variation";
  input.value = 10;
  input.placeholder = "number of results";
  div.appendChild(input);
}

// create input for start_date
function create_input_date_product_with_biggest_variation(div, id) {
  // create date selector
  var input = document.createElement("input");
  input.type = "date";
  input.id = id;
  // giv default value
  switch (id) {
    case "start_date":
      input.value = "2010-01-01";
      break;
    case "end_date":
      input.value = "2010-12-31";
      break;
    case "start_date2":
      input.value = "2011-01-01";
      break;
    case "end_date2":
      input.value = "2011-12-31";
      break;
  }

  div.appendChild(input);
}

// create select for ascending
function create_select_ascending_product_with_biggest_variation(div) {
  var select = document.createElement("select");
  select.id = "ascending";
  var option = document.createElement("option");
  option.value = 1;
  option.text = "Worst to best";
  select.appendChild(option);
  var option = document.createElement("option");
  option.value = 0;
  option.text = "Best to worst";
  select.appendChild(option);
  div.appendChild(select);
}

function create_result_table_variation() {
  var div = document.createElement("div");
  div.className = "table-wrapper";
  var table = document.createElement("table");
  table.id = "result_variation";
  table.className = "fl-table";
  div.appendChild(table);
  // get right div
  var main = document.getElementById("main");
  main.appendChild(div);
}

function create_result_table_variation_sidebar() {
  var div = document.createElement("div");
  div.className = "table-wrapper";
  var table = document.createElement("table");
  table.id = "result_variation";
  table.className = "fl-table";
  div.appendChild(table);
  // get right div
  var main = document.getElementById("sidebar");
  main.appendChild(div);
}

function create_function_selectors_product_with_biggest_variation() {
  var main = document.getElementById("main");
  var div = document.createElement("div");
  div.className = "function_selectors";
  text = document.createTextNode("Product with biggest variation");
  div.appendChild(text);
  create_input_date_product_with_biggest_variation(div, "start_date");
  create_input_date_product_with_biggest_variation(div, "end_date");
  create_input_date_product_with_biggest_variation(div, "start_date2");
  create_input_date_product_with_biggest_variation(div, "end_date2");
  create_input_number_product_with_biggest_variation(div);
  create_select_ascending_product_with_biggest_variation(div);
  create_button_product_with_biggest_variation(div);
  main.appendChild(div);
  create_result_table_variation();
}

create_function_selectors_product_with_biggest_variation();
// call_function_product_with_biggest_variation(
//   "2010-01-01",
//   "2010-12-31",
//   "2011-01-01",
//   "2011-12-31",
//   10,
//   1
// );

function create_function_selectors_product_with_biggest_variation_sidebar() {
  var main = document.getElementById("sidebar");
  var div = document.createElement("div");
  div.className = "function_selectors";
  main.appendChild(div);
  create_result_table_variation_sidebar();

  call_function_product_with_biggest_variation(
    "2010-01-01",
    "2010-12-31",
    "2011-01-01",
    "2011-12-31",
    10,
    1
  );
}

// create_function_selectors_product_with_biggest_variation_sidebar();

function display_modelisation(id, function_name) {
  if (document.getElementById("modelisation_image") != null) {
    document.getElementById("modelisation_image").remove();
  }
  var div = document.getElementById("main");
  var img = document.createElement("img");
  img.id = "modelisation_image";
  // url is modelisation/function_name?id=id
  img.src = "http://localhost:5000/modelisation/" + function_name + "?id=" + id;
  div.appendChild(img);
}

function create_select_function_name_modelisation() {
  var select = document.createElement("select");
  select.id = "function_name_modelisation";
  for (var i = 0; i < array_of_functions_name_modelisation.length; i++) {
    var option = document.createElement("option");
    option.value = array_of_functions_name_modelisation[i];
    option.text = array_of_functions_name_modelisation[i];
    select.appendChild(option);
  }
  div = document.getElementById("main");
  div.appendChild(select);
}

create_select_function_name_modelisation(document.getElementById("sidebar"));

// button call function
function create_button_modelisation() {
  var button = document.createElement("button");
  button.innerHTML = "Call function";
  button.onclick = function () {
    // generate id
    var id = Math.floor(Math.random() * 1000000000);

    var function_name = document.getElementById(
      "function_name_modelisation"
    ).value;
    display_modelisation(id, function_name);
  };
  div = document.getElementById("main");
  div.appendChild(button);
}

create_button_modelisation();

// display_modelisation(10, "plot_top_customers");
