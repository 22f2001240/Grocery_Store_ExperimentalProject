<template>
    <div class="container mt-5" >
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header  text-center">
                        User Signup
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="signupUser">
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input type="text" class="form-control mb-3" id="name" v-model="name" placeholder="Enter name" required>
                            </div>
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input type="email" class="form-control mb-3" id="email" v-model="email" placeholder="Enter email" required>
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input type="password" class="form-control mb-3" id="password" v-model="password" placeholder="Password" required>
                            </div>
                            <div v-if="errormsg" class="text-danger">{{ errormsg }}</div>
                            <div v-if="successmsg" class="text-success">{{ successmsg }}</div>
                            <br>
                            <button type="submit" class="btn btn-primary">Signup</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                name: '',
                email: '',
                password: '',
                errormsg: null,
                successmsg: null,
            }
        },
        methods: {
            async signupUser(){
                this.errormsg = null;
                this.successmsg = null;
                const payload = {
                    email_id: this.email,
                    password: this.password,
                    name: this.name,
                    role: 'customer'
                };
                try {
                    const response =await fetch("/api/signup",
                        {
                            method: 'POST',
                            headers: {'Content-Type' : 'application/json'},
                            body: JSON.stringify(payload)
                    });
                    const result = await response.json();
                    if(!response.ok) {
                        this.errormsg = result.message || "Something went wrong";
                    }else{
                        alert("Signup successful, please login !!");
                        this.successmsg = result.message 
                        this.$router.push('/user-login');
                    }
                }catch(error){
                    this.errormsg = "Unable to connect to server";
                };
            }
        }
    }
</script>
