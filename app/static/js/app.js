const vm = new Vue({
  el: '#app',
  data: {
    name: '',
    email: '',
    password: '',
    token: '',
    signedIn: false,
    jobs: [],
    workers: [],
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
      this.name = localStorage.name;
      this.fetchSummary();
      if (this.token){
        this.fetchJobsWorkers();
        this.signedIn = true;
      }
    },
    onLogin: function() {
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
               this.name = response.data.name;
               localStorage.token = response.data.token;
               localStorage.email = this.email;
               localStorage.name = this.name;
               console.log(this.token);
               this.signedIn = true;
               this.password = '';
               this.fetchJobsWorkers();
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
    fetchJobsWorkers: async function() {
      try {
        let response = await axios.get('/api/jobs/',
                {headers: {'Authorization': "Bearer " + this.token}});
        this.jobs = response.data; 
      } catch (error) { this.handleError(error); };
      /*
      try {
        let response = await axios.get('/api/workers/',
                {headers: {'Authorization': "Bearer " + this.token}});
        this.workers= response.data; 
      } catch (error) { this.handleError(error); };
      */
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
        switch (this.msg) {
          case 'Authentication failed.':
            this.token = '';
            this.signedIn = false;
            break;
          default:
            this.token = '';
            this.signedIn = false;
        }
      } else if (e.request){
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser
        console.log(error.request);
      }
    },
  }
});
