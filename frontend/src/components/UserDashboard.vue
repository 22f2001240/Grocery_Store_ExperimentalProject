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
                            <router-link to="/user-dashboard" class="nav-link active" aria-current="page">Home</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/customer-orders" class="nav-link">Orders</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/customer-cart" class="nav-link">Cart</router-link>
                        </li>
                    </ul>
                    <button class="btn btn-outline-light me-2" @click="logout">Logout</button>
                </div>
            </div>
        </nav>
        <div class="container mt-5"> 
            <div class="card">
                <div class="card-header" style="font-weight: bold; font-size: 1.5rem;"> 
                    Products 
                </div>
                <div class="card-body" >
                <!-- search tab -->
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" placeholder="Search for products..." v-model="searchQuery" />
                    </div>
                    
                    <table v-if="filterProducts.length !==0" class="table table-striped">
                        <thead>
                            <tr>
                                <th> Name</th>
                                <th> Description</th>
                                <th> Price</th>
                                <th> Unit</th>
                                <th> Stock</th>
                                <th> Category</th>
                                <th> Quantity</th>
                                <th> Action</th>
                            </tr>
                        </thead>
                        <tbody> 
                            <tr v-for=" product in filterProducts" :key="product.id"> 
                                <td> {{ product.name }}</td>
                                <td> {{ product.description }}</td>
                                <td> {{ product.price }}</td>
                                <td> {{ product.unit }}</td>
                                <td> {{ product.stock }}</td>
                                <td> {{ product.category_name }}</td>
                                <td> 
                                    <input type="number" v-model="product.quantity" class="form-control" min="1" :max="product.stock" />
                                </td>
                                <td> 
                                    <button type="submit" class="btn btn-success" @click="addToCart(product.id,product.quantity)" > Add to Cart</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <p v-else>No products found 😢</p>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                products: [],
                product : {
                    quantity: null,
                },
                searchQuery: ''
            }
        },
        computed: {
            filterProducts() {
                let allProducts = this.products 
                if(this.searchQuery){
                    allProducts = allProducts.filter(product => 
                        product.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                        product.description.toLowerCase().includes(this.searchQuery.toLowerCase())
                    );
                }
                return allProducts;
            }
        },
        methods : {
            async logout () {
                localStorage.removeItem('userToken')
                await this.$router.push('/')
            },
            fetchProducts: function () {
                const response = fetch('/api/product', {
                    method: 'GET',
                    headers: {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                })
                .then ((response) =>  response.json())
                .then (data =>{
                    this.products = data
                }).catch (error => {
                    console.log(error);
                })
            },
            async addToCart(id,quantity) {
                try {
                    const response = await fetch('/api/cart',{
                        method: 'POST',
                        headers: {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                        },
                        body:JSON.stringify({product_id:id,quantity:quantity})
                    });
                    const result = await response.json();
                    if(response.ok) {
                        alert(result.message);
                        this.fetchProducts();
                        // this.fetchCart()
                    } else { 
                        alert("Error adding to cart: " + result.message);
                    }
                }catch (error) {
                    alert("Error adding to cart: " + error.message);
            }
            } 
        },
        mounted () {
            this.fetchProducts();
        }
    }
</script>