
<template>
    <div class="container mt-5" >
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header  text-center">
                        Admin Login
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="loginAdmin">
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input type="email" class="form-control" id="email" v-model="email" placeholder="Enter email" required>
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" id="password" v-model="password" placeholder="Password" required>
                            </div>
                            <div v-if="errormsg" class="text-danger">{{ errormsg }}</div>
                            <button type="submit" class="btn btn-primary">Login</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script>
export default { //export the data which we used as varibles in template.
    data(){
        return {
            email: '',
            password: '',
            errormsg: null,
        };
    },
    methods: {
        async loginAdmin(){
            this.errormsg = null;  //Initially when we are clicking on the login button it set the error message as null
            const payload = {     //Payloads for the api. Sending this things to the password. So use the same variables which is mentioned here and backend
                email_id: this.email,
                password: this.password
            };
            try{
                const response = await fetch("/api/login",{
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                if(!response.ok){
                    //handle errors
                    this.errormsg = result.message || "Something went wrong"; //if result not having its error msg from backend code, then it will take  something went wrong
                }else{
                    //handle success
                    if(result.user_role == "admin"){
                        alert("Login Successful")
                        localStorage.setItem('adminToken',result.token);  //stored in the local storage in browser
                        this.$router.push('/admin-dashboard') // this will push to admin dashboard.
                    } else {
                        alert("You are not authorized to access this page!")
                    }
                }
            } catch(error) {
                this.errormsg = "Unable to connect to server"; //if there is any error in network (the url not working except 404,405) then it will show network error.
            }
        },
    },
};
</script>
