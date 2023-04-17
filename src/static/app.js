Vue.component('nav-bar', {
    props: ['username'],
    template: `<nav class="navbar navbar-expand-lg navbar-light" style="background-color: #e4e4e4;"> 
    <div class="container-fluid">
    <a class="navbar-brand" href="/">Home</a>
        <span class="navbar-text">
            Welcome back, {{username}}
        </span>
        <!-- Clear the local storage auth token and logout the user -->
        <a href="/logout"class="btn btn-outline-danger">logout</button>
    </div>
    </nav>`
  })
  
  var app = new Vue({
      el: '#app',
      data: {
        username: "Hi"
      }
    })
  