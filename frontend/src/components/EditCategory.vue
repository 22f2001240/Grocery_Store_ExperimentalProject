<template>
    <div class="container mt-5" >
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header  text-center">Edit Category</div>
                    <div class="card-body">
                        <form @submit.prevent="editCategory">
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input type="text" class="form-control" id="name" v-model="name" :placeholder="category_name" required>
                            </div><br>
                            <button type="submit" class="btn btn-primary">Save Changes</button>
                            <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
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
                errorMessage: '',
                category_name: '',
            }
        },
        methods: {
            async editCategory() {
                const payload = {
                    name : this.name,
                };
                try {
                    const response = await fetch(`/api/category/${this.$route.params.id}`,{
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                        },
                        body: JSON.stringify(payload),
                    });
                    const result = await response.json();
                    if(!response.ok) {
                        this.errorMessage = result.message || "Something went wrong";
                    } else {
                        alert(result.message);
                        this.$router.push('/admin-dashboard');
                    }
                } catch (error) {
                    alert("Something went wrong")
                }
            },
            async fetchCategory() {
                try {
                    const response = await fetch(`/api/category/edit/${this.$route.params.id}`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
                        }
                    });
                    const result = await response.json();
                    if(!response.ok) {
                        this.errorMessage = result.message || "Something went wrong";
                    } else {
                        this.category_name = result.name;
                    }
                } catch (error) {
                    alert("Something went wrong")
                }
            },
        },
        mounted() {
            this.fetchCategory();
        }
    }
</script>
