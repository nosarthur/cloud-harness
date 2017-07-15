
var vm = new Vue({
  el: '#app',
  data: {
    email: '',
    password: '',
    token: '',
    signedIn: false,
    jobs: [],
    summary: null,
    error: null,
    msg: '',
  },
  created() {
    this.checkLogin();
  },
  methods: {
    checkLogin: function() {
      this.token = localStorage.token;
      this.email = localStorage.email;
      this.fetchSummary();
      if (this.token){
        this.fetchJobs();
        this.signedIn = true;
      }
    },
    onLogin: function() {
      console.log(this.email);
      // form validation
      if (!this.password){
        return;
      }
      axios.post('/auth/login',
                 {email: this.email, password: this.password},)
           .then(response => {
             this.msg = response.data.msg;
             if (response.data.token){
               this.token = response.data.token;
               localStorage.token = response.data.token;
               localStorage.email = this.email;
               console.log(this.token);
               this.signedIn = true;
               this.password = '';
               this.fetchJobs();
             }
           })
           .catch(error => { this.handleError(error); });
    },
    onLogout: function(){
      axios.get('/auth/logout',
                 {headers: {'Authorization': "Bearer " + this.token}})
           .then(response => {
             this.signedIn = false;
             this.msg = response.data.msg;
             this.token = '';
             localStorage.token = '';
           })
           .catch(error => { this.handleError(error); });
    },
    fetchJobs: function() {
      axios.get('/api/jobs/',
                {headers: {'Authorization': "Bearer " + this.token}})
           .then(response => {
             this.jobs = response.data; 
           })
           .catch(error => { this.handleError(error); });
    },
    fetchSummary: function() {
      axios.get('/api/summary')
           .then(response => {
             this.summary = response.data; 
           })
           .catch(error => { console.log(error); });
    },
    handleError: function(e) {
      if (e.response){
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        this.msg = e.response.data.message;
        console.log(this.msg);
      } else if (e.request){
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser
        console.log(error.request);
      }
      //this.token = '';
      this.signedIn = false;
    },
  }
});
