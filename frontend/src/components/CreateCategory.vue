<template>
    <div class="container mt-5" >
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header  text-center">Create Category</div>
                    <div class="card-body">
                        <form @submit.prevent="createCategory">
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input type="text" class="form-control" id="name" v-model="name" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Add Category</button>
                            <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
                        </form>
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
                name: '',
                errorMessage: null,
            }
        },
        methods: {
            async createCategory() {
                const payload = {
                    name: this.name,
                };
                try {
                    const response = await fetch('/api/category',{
                        method: 'POST',
                        headers: {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                        },
                        body: JSON.stringify(payload)
                    });
                    const result = await response.json();
                    if(!response.ok) {
                        this.errorMessage = result.message || "Something went wrong"
                    } else {
                        alert(result.message)
                        this.$router.push('/admin-dashboard')
                    }
                } catch (error) {
                    this.errorMessage = "Unable to connect to the server";
                }
            }
        }
    }
</script>
