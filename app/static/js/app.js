var vm = new Vue({
  el: '#app',
  data: {
    email: '',
    password: '',
    token: '',
    signedIn: false,
    jobs: [],
    summary: '',
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
        if (this.jobs){
          this.signedIn = true;
        }
      }
    },
    onLogin: function() {
      console.log(this.email);
      axios.post('/auth/login',
                 {email: this.email, password: this.password},)
           .then(response => {
             if (response.data.token){
               this.token = response.data.token;
               localStorage.token = response.data.token;
               localStorage.email = this.email;
               console.log(this.token);
               this.signedIn = true;
               this.fetchJobs();
             }
           })
           .catch(error => {console.log(error);})
    },
    onLogout: function(){
      axios.get('/auth/logout',
                 {headers: {'Authorization': "Bearer " + this.token}})
           .then(response => {
             this.signedIn = false;
             this.token = '';
             this.password = '';
             localStorage.token = '';
           })
           .catch(error => {console.log(error);})
    },
    fetchJobs: function() {
      axios.get('/api/jobs/',
                {headers: {'Authorization': "Bearer " + this.token}})
           .then(response => {
             this.jobs = response.data; 
           })
           .catch(error => {console.log(error);})
    },
    fetchSummary: function() {
      axios.get('/api/jobs/summary/')
           .then(response => {
             this.summary = response.data; 
           })
           .catch(error => {console.log(error);})
    },
  }
});
