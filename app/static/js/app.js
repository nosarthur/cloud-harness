var vm = new Vue({
  el: '#app',
  data: {
    email: '',
    password: '',
    token: '',
    signedIn: false,
    jobs: [],
    summary: ' summary',
  },
  created() {
    this.checkLogin();
  },
  methods: {
    checkLogin: function() {
      this.token = localStorage.token;
      this.email = localStorage.email;
      if (this.token){
        this.fetchData();
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
               this.fetchData();
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
    fetchData: function() {
      axios.get('/api/jobs/',
                {headers: {'Authorization': "Bearer " + this.token}})
           .then(response => {
             this.summary = response.data.length; 
             this.jobs = response.data; 
           })
           .catch(error => {console.log(error);})
    },
  }
});
