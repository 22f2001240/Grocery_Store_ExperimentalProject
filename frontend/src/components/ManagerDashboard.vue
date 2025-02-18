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
                            <router-link to="/manager-dashboard" class="nav-link active" aria-current="page">Home</router-link>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" aria-current="page" @click="exportData">Export CSV</a>
                        </li>
                    </ul>
                    <button class="btn btn-outline-light me-2" @click="logout">Logout</button>
                </div>
            </div>
        </nav>
        <div class="container mt-5">
            <div class="card">
                <div class="card-header" style="font-weight: bold; font-size: 1.5rem;">Products</div>
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Name</th>
                                <th scope="col">Description</th>
                                <th scope="col">Price</th>
                                <th scope="col">Unit</th>
                                <th scope="col">Stock</th>
                                <th scope="col">Sold</th>
                                <th scope="col">Category</th>
                                <th scope="col">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="product in products" :key="product.id">
                                <th scope="row">{{ product.id }}</th>
                                <td>{{ product.name }}</td>
                                <td>{{ product.description }}</td>
                                <td>{{ product.price }}</td>
                                <td>{{ product.unit }}</td>
                                <td>{{ product.stock }}</td>
                                <td>{{ product.number_of_sold_items }}</td>
                                <td>{{ product.category_name }}</td>
                                <td >
                                    <router-link :to="'/edit-product/'+product.id" class="btn btn-info">Edit</router-link>
                                    <button @click="DeleteProduct(product.id)" class="btn btn-danger">Delete</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div><br><br>

<!-- Category request table  -->
        <div class="container mt-5">
            <div class="card">
                <div class="card-header" style="font-weight: bold; font-size: 1.5rem;">Category Requests</div>
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Action</th>
                                <th scope="col">Category ID</th>
                                <th scope="col">Requested Name</th>
                                <th scope="col">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="request in category_requests" :key="request.id">
                                <th scope="row">{{ request.id }}</th>
                                <td>{{ request.action }}</td>
                                <td>{{ request.category_id }}</td>
                                <td>{{ request.name }}</td>
                                <td>{{ request.status }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div><br><br>

<!-- Create product form  -->
        <div class="container mt-5 d-flex " style="max-width: 50vw;">
            <div class="card w-100">
                <div class="card-header " style="font-weight: bold; font-size: 1.5rem;">Create Product</div>
                <div class="card-body d-flex flex-column">
                    <form @submit.prevent="addProduct" class="w-100">
                        <div class="form-group">
                            <label for="name">Name</label>
                            <input type="text" class="form-control mb-3 w-100" id="name" v-model="new_product.name" required>
                        </div>
                        <div class="form-group">
                            <label for="description">Description</label>
                            <input type="text" class="form-control mb-3 w-100" id="description" v-model="new_product.description" required>
                        </div>
                        <div class="form-group">
                            <label for="price">Price</label>
                            <input type="number" class="form-control mb-3 w-100" id="price" v-model="new_product.price" required>
                        </div>
                        <div class="form-group">
                            <label for="unit">Unit</label>
                            <input type="text" class="form-control mb-3 w-100" id="unit" v-model="new_product.unit" required>
                        </div>
                        <div class="form-group">
                            <label for="name">Stock</label>
                            <input type="number" class="form-control mb-3 w-100" id="name" v-model="new_product.stock" required>
                        </div>
                        <div class="form-group">
                            <label for="category_id">Choose category</label>
                            <select class="form-select mb-3 w-100" id="category_id" v-model="new_product.category_id" required>
                                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
                            </select>
                        </div>
                        <div v-if="errorMessages" class="text-danger">{{ errorMessages }}</div>
                        <button type="submit" class="btn btn-primary">Add Product</button>
                    </form>
                </div>
            </div>
        </div><br><br>
        <!-- creating a form for requesting CRUD for a category -->
        <div class="container"> 
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header" style="font-weight: bold; font-size: 1.5rem;">
                            Manage Category
                        </div>
                        <div class="card-body">
                            <form @submit.prevent="categoryCRUDRequest(category_request.action)">
                                <div class="form-group">
                                    <label for="action">Action</label>
                                    <select class="form-select " id="action" v-model="category_request.action" required>
                                        <option value="CREATE">Create</option>
                                        <option value="UPDATE">Update</option>
                                        <option value="DELETE">Delete</option>
                                    </select>
                                </div>
                                <div v-if="category_request.action !== 'CREATE'" class="form-group">
                                    <label for="category">Select Category</label>
                                    <select class="form-control" id="category" v-model="category_request.category_id" required>
                                        <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
                                    </select>
                                </div><br>
                                <div v-if="category_request.action !== 'DELETE'" class="form-group">
                                    <label for="category_id">Name</label>
                                    <input type="text" class="form-control " id="name" v-model="category_request.name" required/>
                                </div>
                                
                                <button type="submit" class="btn btn-primary">Send Request</button>
                                <div v-if="errorMessages" class="text-danger">{{ errorMessages }}</div>
                            </form> 
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <br><br><br>

    </div>
</template>


<script>
    export default {
        data() {
            return {
                products:[],
                categories: [],
                category_requests:[],
                new_product:{
                    name: '',
                    description: '',
                    price: 0,
                    unit: '',
                    stock: 0,
                    category_id: '',
                },
                category_request:{
                    action: 'CREATE',
                    category_id: '',
                    name: '',
                },
                errorMessages: null,
            }
        },
        methods: {
            async logout() {
                localStorage.removeItem('managerToken');
                this.$router.push('/')
            },
            async categoryCRUDRequest(action) {
                try {
                    const response = await fetch('/api/category/request', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('managerToken')}`
                        },
                        body: JSON.stringify(this.category_request)
                    });
                    const result = await response.json();
                    if (response.ok) {
                        alert(result.message);
                        this.fetchCategoryRequests();
                        this.category_request = {
                            action: 'CREATE',
                            category_id: '',
                            name: '',
                        };
                    } else {
                        alert(result.message);
                    }
                } catch (error) {
                    alert("Error sending request");
                    console.log(error);
                }
            },
            async DeleteProduct(id) {
                const isConfirmed = window.confirm('Are you sure you want to delete this product?')
                if (!isConfirmed) {
                    return
                };
                try {
                    const response = await fetch(`/api/product/${id}`,{
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('managerToken')}`
                        }
                    });
                    const result = await response.json();
                    if (response.ok) {
                        alert(result.message);
                        this.fetchProducts();
                    } else {
                        alert(result.message);
                    }
                } catch(error) {
                    alert("Error deleting product");
                }
            },
            async addProduct() {
                try {
                    const response = await fetch('/api/product',{
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('managerToken')}`
                        },
                        body: JSON.stringify(this.new_product)
                    });
                    if (response.ok) {
                        const result = await response.json();
                        alert(result.message);
                        this.fetchProducts();
                    } else {
                        alert("Error adding product");
                    }
                } catch (error) {
                    alert("Error adding product");
                }
            },
            fetchProducts: function(){
                const response = fetch('/api/manager/product',{
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('managerToken')}`
                    }
                })
                .then((response) => response.json())
                .then(data => {
                    this.products = data;
                })
                .catch(error => {
                    console.log(error);
                })
            },
            fetchCategories: function() {
                const response = fetch(`/api/category`, {
                    method: 'GET',
                    headers: {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('managerToken')}`
                    }
                })
                .then ((response) => response.json())
                .then(data => {
                    this.categories = data;
                }).catch(error => {
                    console.log(error);
                })
            },
            fetchCategoryRequests: function(){
                const response = fetch('/api/category/request',{
                    method: 'GET',
                    headers: {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('managerToken')}`
                    }
                })
                .then((response) => response.json())
                .then(data => {
                    this.category_requests = data;
                })
                .catch(error => {
                    console.log(error);
                })
            },
            async exportData() {
                try {
                    const response = await fetch('/api/product/export',{
                        method: 'GET',
                        headers: {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('managerToken')}`
                        }
                    });
                    const result = await response.json();
                    if(response.ok) {
                        alert(result.message)
                    } else {
                        alert(result.message);
                    }
                } catch (error) {
                    alert("Error exporting data");
                    console.log(error);
                }
            }
            },
            mounted() {
                this.fetchProducts();
                this.fetchCategories();
                this.fetchCategoryRequests();
            }
        }
</script>
