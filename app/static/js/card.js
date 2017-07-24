
Vue.component('job-card', {
  props: ['job'],
  template: ` <div class="col-sm-3">
                <div class="panel panel-default">
                <div class="panel-heading">
                  <h3 class="panel-title">
                    {{job.id}} {{ job.status }} 
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
              </div> `
})
