function collect_data() {
  return {
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    username: document.getElementById("username").value,
    posting_time: document.getElementById("posting_time").value,
  };
}

eel.expose(report_output)
function report_output(print_statement) {
    let print_space = document.getElementById("output");
    let allText = print_space.innerHTML + print_statement;
    print_space.innerHTML = allText.substr(allText.length - 30000);
    print_space.scrollTop = print_space.scrollHeight;
}

let login_button = document.getElementById("login");
 login_button.addEventListener("click", function() {
    login_button.disabled = true;
    let user_data = collect_data()
    eel.tweet_details(user_data)(function() {
      document.getElementById("output").innerHTML = result;
      login_button.disabled = false;
  });
 })

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener("contextmenu", event => event.preventDefault());
    eel.write_output();

})