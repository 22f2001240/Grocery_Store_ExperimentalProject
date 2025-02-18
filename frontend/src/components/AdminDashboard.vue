<template>
    <div>
        <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Grocery Store</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <router-link to="/admin-dashboard" class="nav-link active" aria-current="page">Home</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/create-category" class="nav-link">Create Category</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/unapproved-managers" class="nav-link">Unapproved Managers</router-link>
                        </li>
                        
                    </ul>
                    <button class="btn btn-outline-light me-2" @click="logout">Logout</button>
                </div>
            </div>
        </nav>
        <div class="container mt-5">
            <div class="card">
                <div class="card-header" style="font-weight: bold; font-size: 1.5rem;">
                    Managers
                </div>
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Name</th>
                                <th scope="col">Email-ID</th>
                                <th scope="col">Status</th>
                                <th scope="col">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="manager in managers" :key="manager.id">
                                <th scope="row">{{ manager.id }}</th>
                                <td>{{ manager.name }}</td>
                                <td>{{ manager.email_id }}</td>
                                <td>{{ manager.status }}</td>
                                <td v-if="manager.status=='pending'">
                                    <button @click="ApproveManager(manager.id)" class="btn btn-success">Approve</button>
                                    <button @click="RejectManager(manager.id)" class="btn btn-danger">Reject</button>
                                </td>
                                <td v-else>
                                    <button @click="ApproveManager" class="btn btn-success" disabled>Approved</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <br><br>
        <div class="container mt-2">
            <div class="card">
                <div class="card-header" style="font-weight: bold; font-size: 1.5rem;">
                    Categories
                </div>
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Name</th>
                                <th scope="col">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="category in categories" :key="category.id">
                                <th scope="row">{{ category.id }}</th>
                                <td>{{ category.name }}</td>
                                <td>
                                    <router-link :to="'/edit-category/'+category.id" class="btn btn-info">Edit</router-link>
                                    <button @click="DeleteCategory(category.id)" class="btn btn-danger">Delete</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <br><br>
<!-- Table for category requests -->
        <div class="container mt-2">
            <div class="card">
                <div class="card-header" style="font-weight: bold; font-size: 1.5rem;">
                    Category Requests
                </div>
                <div class="card-body">
                    <div v-if="requests.length === 0">
                        Currently no category requests!
                    </div>
                    <div v-else>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">ID</th>
                                    <th scope="col">Category_id</th>
                                    
                                    <th scope="col">Action</th>
                                    <th scope="col">Requested name</th>
                                    <th scope="col">Requested manager</th>
                                    <th scope="col">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="request in requests" :key="request.id">
                                    <th scope="row">{{ request.id }}</th>
                                    <td>{{ request.category_id }}</td>
                                    
                                    <td>{{ request.action }}</td>
                                    <td>{{ request.name }}</td>
                                    <td>{{ request.manager_name }}</td>
                                    <td>{{ request.status }}</td>
                                    <td>
                                        <button @click="approve(request.id)" type="submit" class="btn btn-success">Approve</button>
                                        <button @click="reject(request.id)" type="submit" class="btn btn-danger">Reject</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div><br><br><br>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                managers: [],
                categories: [],
                requests:[],
                errorMessage: null,
            }
        },
        methods: {
            async logout() {
                localStorage.removeItem('adminToken');
                this.$router.push('/');
            },
            async DeleteCategory(id) {
                const isConfirmed = window.confirm("Are you sure you want to delete this category?");
                if (!isConfirmed) {
                    return; // Stop the function if the admin cancels the deletion
                }
                
                try {
                    const response = await fetch(`/api/category/${id}`,{
                        method : 'DELETE',
                        headers : { 
                            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                            'Content-Type' : 'application/json'
                        }
                    });
                    if(response.ok) {
                        const result = await response.json();
                        alert(result.message);
                        // To get reload the category table after delete
                        this.fetchCategories();
                        this.$router.push('/admin-dashboard');
                    } else {
                        alert("Error deleting category")
                    }
                } catch (error) {
                    alert('Error deleting category');
                }
            },
            
            fetchCategories: function() {
                const response = fetch('/api/category',
                    {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                            'Content-Type': 'application/json',
                        }
                    }
                )
                .then((response) => response.json())
                .then(data => {
                    this.categories = data;
                })
                .catch(error => {
                    console.log(error);
                })
            },
            fetchManagers: function() {
                const response = fetch('/api/login',{
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                        'Content-Type': 'application/json',
                    }
                })
                .then((response) => response.json())
                .then(data => {
                    this.managers = data;
                })
                .catch(error => {
                    console.log(error);
                })
            },
            async ApproveManager(id) {
                try {
                    const response = await fetch(`/api/approve/${id}`,{
                        method : 'PATCH',
                        headers : { 
                            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                            'Content-Type' : 'application/json'
                        }
                    });
                    if(response.ok) {
                        const result = await response.json();
                        alert(result.message);
                        // To get reload the category table after delete
                        this.fetchManagers();
                        this.$router.push('/admin-dashboard');
                    } else {
                        alert(result.message)
                    }
                } catch (error) {
                    alert('Error approving manager');
                }
            },
            fetchCategoryRequests: function() {
                const response = fetch('/api/category/request',{
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                        'Content-Type': 'application/json',
                    }
                })
                .then((response) => response.json())
                .then(data => {
                    this.requests = data;
                }).catch(error => {
                    console.log(error)
                })
            },
            async approve(id) {
                try {
                    const response = await fetch('/api/category/request/action',{
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            request_id: id,
                            action: 'APPROVE',
                        })
                    });
                    const result = await response.json();
                    if(response.ok) {
                        alert(result.message);
                        // To get reload the category table after delete
                        this.fetchCategoryRequests();
                        this.fetchCategories();
                        this.$router.push('/admin-dashboard');
                    } else {
                        alert(result.message)
                    }
                } catch (error) {
                    alert(error.message);
                }
            },
            async reject(id) {
                try {
                    const response = await fetch('/api/category/request/action',{
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            request_id: id,
                            action: 'REJECT',
                        })
                    });
                    const result = await response.json();
                    if(response.ok) {
                        alert(result.message);
                        // To get reload the category table after delete
                        this.fetchCategoryRequests();
                        this.fetchCategories();
                        this.$router.push('/admin-dashboard');
                    } else {
                        alert(result.message)
                    }
                } catch (error) {
                    alert(error.message);
                }
            }
        },
        // To get the data when the app is loaded once
        mounted() {
            this.fetchManagers();
            this.fetchCategories();
            this.fetchCategoryRequests();
        }
    }
</script>


