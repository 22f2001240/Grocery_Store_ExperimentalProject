<template>
    <div>
        <div class="container mt-5 d-flex " style="max-width: 50vw;">
            <div class="card w-100">
                <div class="card-header " style="font-weight: bold; font-size: 1.5rem;">Edit Product</div>
                <div class="card-body d-flex flex-column">
                    <form @submit.prevent="editProduct" class="w-100">
                        <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" class="form-control mb-3 w-100" id="name" v-model="new_product.name" :placeholder="new_product.price" required>
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
                    <button type="submit" class="btn btn-primary">Update Product</button>
                    <router-link to="/manager-dashboard" class="btn btn-secondary mx-3"> Cancel</router-link> 
                    </form>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        data() {
            return {
                products:[],
                categories: [],
                new_product:{
                    name: '',
                    description: '',
                    price: 0,
                    unit: '',
                    stock: 0,
                    category_id: '',
                },
                errorMessages: null,
            }
        },
        methods: {
            async editProduct() {
                try {
                    const response = await fetch(`/api/product/${this.$route.params.id}`,{
                        method: 'PUT',
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
                        this.$router.push('/manager-dashboard')
                    } else {
                        alert("Error adding product");
                    }
                } catch (error) {
                    alert("Error adding product");
                }
            },
            async fetchProducts() {
                try {
                    const response = await fetch('/api/manager/product', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('managerToken')}`
                        }
                    });

                    if (!response.ok) throw new Error("Failed to fetch products");

                    this.products = await response.json();
                } catch (error) {
                    console.error(error);
                }
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
            // Create a function for retrieving the complete data of current product.
            async fetchCurrentProduct(id) {
                // Fetch the product data from the API using the provided ID.
                const product = this.products.find(product => product.id == id);
                if(product) {
                    console.log(id)
                    this.new_product = product
                } else {
                    
                    
                }
            }
        },
        watch: {
            products(newProducts) {
                if (newProducts.length > 0) {
                    this.fetchCurrentProduct(this.$route.params.id);
                }
            }
        },
        mounted() {
                this.fetchProducts();
                this.fetchCategories();
                // this.fetchCurrentProduct(this.$route.params.id);
            }
    }
</script>
