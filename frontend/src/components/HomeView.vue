<template>
    <div class="container d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div class="card">
            <div class="card-header text-center">
                Welcome to Grocery Store
            </div>
            <div class="card-body">
                <h5 class="card-title text-center">Select your role</h5>
                <blockquote class="blockquote mb-0 d-flex justify-content-center">
                    <router-link to="/admin-login" class="btn btn-primary mx-2">Admin</router-link>
                    <router-link to="/user-login" class="btn btn-primary mx-2">User</router-link>
                    <router-link to="/manager-login" class="btn btn-primary mx-2">Manager</router-link>
                </blockquote>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HomeView'
};
</script>
