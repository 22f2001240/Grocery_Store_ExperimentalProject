<template>
    <div class="container mt-5" >
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header  text-center">
                        User Login
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="loginUser">
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input type="email" class="form-control" id="email" v-model="email" placeholder="Enter email" required>
                            </div>
                            <div class="form-group mt-3">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" id="password" v-model="password" placeholder="Password" required>
                            </div>
                            <div v-if="errormsg" class="text-danger mt-3">{{ errormsg }}</div>
                            <br>
                            <button type="submit" class="btn btn-primary">Login</button>
                            <div class="d-flex justify-content-center mt-3">
                                <router-link to="/user-signup" class="btn btn-primary">Signup</router-link>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default{
        data(){
            return{
                email:'',
                password:'',
                errormsg: null
            }
        },
        methods: {
            async loginUser(){
                this.errormsg = null;
                const payload = {
                    email_id: this.email,
                    password: this.password
                };
                try {
                    const response = await fetch("/api/login",
                        {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(payload)
                        });
                        const result = await response.json();
                        if(!response.ok){
                            this.errormsg = result.message || "Something went wrong";
                        }
                        else{
                            if(result.user_role == 'customer' ){
                            alert("Login Successful")
                            localStorage.setItem('userToken',result.token)
                            this.$router.push('user-dashboard')
                            }else{
                                alert("You are not authorized to access this page!")
                            }
                        }
                }
                catch (error) {
                    this.errormsg = "Unable to connect to server";
                }
            }
        }
    }
</script>
