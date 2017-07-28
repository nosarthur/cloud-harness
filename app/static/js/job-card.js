
Vue.component('job-card', {
  props: ['job'],
  template: ` <div class="col-sm-3">
                <div class="panel panel-default">
                <div class="panel-heading">
                  <h3 class="panel-title">
                    <span>{{job.id}}</span>
                    {{ job.status }} 
                    <button name='start' @click='startJob(job.id)' v-show="job.status=='WAITING'" class='btn btn-success'>Start</button>
                    <button name='stop' @click='stopJob(job.id)' v-show="job.status=='RUNNING'" class='btn btn-warning'>Stop</button>
                  </h3>
                </div>
                <div class="panel-body">
                  <p><span class="badge alert-info"> priority </span>
                    {{ job.priority }}
                  </p>
                  <p><span class="badge alert-danger"> user id: </span>
                     <strong> {{job.user_id}} </strong>
                  </p>
                </div>
              </div>
              </div> `,
  methods: {
    startJob: async function(jobId){
      try {
        let token = localStorage.token;
        let response = await axios.post('/api/jobs/start/' + jobId, {},
                {headers: {'Authorization': "Bearer " + token}});
      } catch (error) { console.log(error); };
    },
    stopJob: async function(jobId){
      try {
        let token = localStorage.token;
        let response = await axios.delete('/api/jobs/stop/' + jobId,
                {headers: {'Authorization': "Bearer " + token}});
      } catch (error) { console.log(error); };
    },
  },
})
