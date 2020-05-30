let ta_input = document.getElementById('ta_input');
let ta_output = document.getElementById('ta_output');
let btn_convert = document.getElementById('btn_convert');
let btn_copy = document.getElementById('btn_copy');
let btn_reset = document.getElementById('btn_reset');
let btn_clear = document.getElementById('btn_clear');

function transform() {
  let text = ta_input.value;
  let newtext = "";
  for (i = 0; i < text.length; ++i) {
    rand = Math.floor(Math.random()*100);
    if (rand < 50) {
      newtext += text[i].toLowerCase();
    } else {
      newtext += text[i].toUpperCase();
    }
  }
  ta_output.value = newtext;
}

function reset() {
  ta_input.value = "";
  ta_output.value = "";
}

function copy() {
  ta_output.select();
  ta_output.setSelectionRange(0, 99999);
  document.execCommand("copy");
  alert("tExT C0pIeD");
}
