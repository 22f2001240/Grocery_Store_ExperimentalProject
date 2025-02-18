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
                    </ul>
                </div>
            </div>
        </nav>
        
        <div class="container mt-5"> 
            <div class="card">
                <div class="card-header" style="font-weight: bold; font-size: 1.5rem;"> 
                    Items in your cart
                </div>
                <div class="card-body" >
                    <div v-if="items.length === 0" >
                        No items in your cart.
                    </div>
                    <div v-else>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th> ID</th>
                                    <th> Name</th>
                                    <th> Quantity</th>
                                    <th> Price per unit</th>
                                </tr>
                            </thead>
                            <tbody> 
                                <tr v-for=" item in items" :key="item.id"> 
                                    <td> {{ item.id }}</td>
                                    <td> {{ item.product_name }}</td>
                                    <td v-if="updateReq" >
                                        <input type="number" v-model="item.quantity" class="form-control" min="1" :max="item.product_stock" /><br>
                                        <!-- <button type="submit" class="btn btn-success" @click="onUpdated(item.id)" >Update</button> -->
                                    </td>
                                    <td v-else> {{ item.quantity }} {{ item.product_unit }}</td>
                                    <td> {{ item.product_price }} </td>
                                    <td> 
                                        <button type="submit" class="btn btn-primary" @click="onUpdated(item.id)">Update</button>
                                        <button type="submit" class="btn btn-danger" @click="deleteItem(item.id)">Remove</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="mt-3 text-center"> 
                            <p style="font-weight: bold; font-size: 1.2rem;">Total cart value: {{ totalPrice }}</p>
                            <button type="submit" class="btn btn-success" @click="makeOrder" > Order Now</button>
                        </div>    
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            items: [],
            totalPrice: null,
            updateReq: false,
        }
    },
    methods: {
        fetchItems: function() {
            const response = fetch('/api/cart', {
                method: 'GET',
                headers: {
                    'Content-Type' : 'application/json',
                    'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                }
            })
            .then((response) => response.json())
            .then(data => {
                // alert(data.cart_products)
                this.items = data.cart_products;
                this.totalPrice = data.total;
            }) .catch(error => {
                console.error('Error:', error);
            });
        },
        async deleteItem(id) {
            try {
                const response = await fetch(`/api/cart/${id}`,{
                    method: 'DELETE',
                    headers: {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                if(response.ok) {
                    const result = response.json();
                    alert("Item deleted successfully");
                    this.fetchItems();
                } else {
                    alert('Error while deleting');
                }
            }catch(error) {
                alert("Error while deleting");
        }
        },
        async onUpdated(id) {
            if(!this.updateReq){
                this.updateReq = true;
            } else {
                this.updateReq = false;
                try {
                    const response = await fetch(`/api/cart/${id}`,{
                        method: 'PATCH',
                        headers: {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                        },
                        body: JSON.stringify({ quantity: this.items.find(item => item.id === id).quantity })
                    })
                    if(response.ok) {
                        const result = await response.json();
                        alert(result.message);
                        this.fetchItems();
                    } else {
                        alert('Error while updating');
                    }
                } catch (error){
                    alert("Error while updating");
                }
            }
        },
        async makeOrder() {
            try {
                const response = await fetch('/api/order',{
                    method: 'POST',
                    headers:{
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json();
                if(response.ok){
                    alert(result.message);
                    this.fetchItems();
                    this.$router.push('/user-dashboard');
                } else {
                    alert(result.message);
                }
            } catch (error) {
                alert("Error while ordering");
            }
        }
    },
    mounted () {
        this.fetchItems();
    }
}
</script>
