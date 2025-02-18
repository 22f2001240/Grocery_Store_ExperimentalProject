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
                            <router-link to="/customer-cart" class="nav-link">Cart</router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="container mt-5"> 
            <div class="card">
                <div class="card-header" style="font-weight: bold; font-size: 1.5rem;"> 
                    Order List
                </div>
                <div class="card-body" >
                    <div v-if="orders.length === 0">
                        No orders found.
                    </div>
                    <div v-else>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th> ID</th>
                                    <th> Name</th>
                                    <th> Quantity</th>
                                    <th> Price per unit</th>
                                    <th> Date of Purchase</th>
                                    <th> Total Price </th>
                                </tr>
                            </thead>
                            <tbody> 
                                <tr v-for=" order in orders" :key="order.id"> 
                                    <td> {{ order.id }}</td>
                                    <td> {{ order.product_name }}</td>                                
                                    <td> {{ order.quantity }} {{ order.product_unit }} </td>
                                    <td> ₹{{ order.product_price }} </td>
                                    <td> {{ order.date_of_purchase }} </td>
                                    <td> ₹{{ (order.quantity * order.product_price)}} </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default{
        data() {
            return {
                orders: []
            }
        },
        methods: {
            fetchOrders: function(){
                const response = fetch('/api/order',{
                    method:'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('userToken')}`
                    }
                })
                .then((response) => response.json())
                .then(data => {
                    this.orders = data
                } ) .catch (error => {
                    console.error('Error:', error);
                })
            }
        },
        mounted() {
            this.fetchOrders();
        }
    }
</script>