<template>
  <div class="product-management">
    <!-- Add New Product Section -->
    <div class="form-section">
      <h2>Add a New Product</h2>
      <form @submit.prevent="addProduct" class="product-form">
        <input v-model="newProduct.name" placeholder="Name">
        <input type="number" v-model.number="newProduct.price" placeholder="Price">
        <input v-model="newProduct.category" placeholder="Category">
        <textarea v-model="newProduct.description" placeholder="Description"></textarea>
        <input v-model="newProduct.image_url" placeholder="Image URL">
        <input type="number" v-model.number="newProduct.discount" placeholder="Discount">
        <input type="number" v-model.number="newProduct.stock_quantity" placeholder="Stock Quantity">
        <input type="checkbox" v-model="newProduct.is_featured"> Featured Product
        <button type="submit">Add Product</button>
      </form>
    </div>

    <!-- Update Existing Product Section -->
    <div class="form-section">
      <h2>Update Existing Product</h2>
      <select v-model="selectedProductId" @change="fetchProductDetails">
        <option disabled value="">Please select one</option>
        <option v-for="product in products" :key="product.id" :value="product.id">{{ product.name }}</option>
      </select>
      <form @submit.prevent="updateProduct" class="product-form">
        <input v-model="updateProductData.name" placeholder="Name">
        <input type="number" v-model.number="updateProductData.price" placeholder="Price">
        <input v-model="updateProductData.category" placeholder="Category">
        <textarea v-model="updateProductData.description" placeholder="Description"></textarea>
        <input v-model="updateProductData.image_url" placeholder="Image URL">
        <input type="number" v-model.number="updateProductData.discount" placeholder="Discount">
        <input type="number" v-model.number="updateProductData.stock_quantity" placeholder="Stock Quantity">
        <input type="checkbox" v-model="updateProductData.is_featured"> Featured Product
        <button type="submit">Update Product</button>
      </form>
    </div>

    <!-- Delete Product Section -->
    <div class="form-section">
      <h2>Delete Product</h2>
      <select v-model="deleteProductId">
        <option disabled value="">Please select one</option>
        <option v-for="product in products" :key="product.id" :value="product.id">{{ product.name }}</option>
      </select>
      <button @click="deleteProduct" class="product-form button">Delete Product</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [], // For fetching and displaying in dropdowns
      newProduct: {
        name: '',
        price: 0,
        category: '',
        description: '',
        image_url: '',
        discount: 0,
        stock_quantity: 0,
        is_featured: false,
      },
      selectedProductId: '', // ID of the selected product for update
      updateProductData: {
        name: '',
        price: 0,
        category: '',
        description: '',
        image_url: '',
        discount: 0,
        stock_quantity: 0,
        is_featured: false,
      },
      deleteProductId: '', // ID of the product to delete
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
  fetchProducts() {
    axios.get('http://localhost:8000/api/shop/products/')
      .then(response => {
        this.products = response.data;
      })
      .catch(error => console.error("Error fetching products:", error));
  },
  fetchProductDetails() {
    const product = this.products.find(p => p.id === this.selectedProductId);
    if (product) {
      this.updateProductData = { 
        ...product, 
      };
    }
  },
  addProduct() {
    axios.post('http://localhost:8000/api/shop/admin/products/add_product/', this.newProduct)
      .then(() => {
        alert('Product added successfully');
        this.fetchProducts(); // Refresh the list after adding
      })
      .catch(error => console.error("Error adding product:", error));
  },
  updateProduct() {
    axios.post(`http://localhost:8000/api/shop/admin/products/${this.selectedProductId}/update_product/`, this.updateProductData)
      .then(() => {
        alert('Product updated successfully');
        this.fetchProducts(); // Refresh the list after updating
      })
      .catch(error => console.error("Error updating product:", error));
  },
  deleteProduct() {
    if (!this.deleteProductId) return;
    axios.post(`http://localhost:8000/api/shop/admin/products/${this.deleteProductId}/delete_product/`)
      .then(() => {
        alert('Product deleted successfully');
        this.fetchProducts(); // Refresh the list after deleting
        this.deleteProductId = ''; // Reset the selection

      })
      .catch(error => console.error("Error deleting product:", error));
  },
}
}
</script>

<style>
.product-management {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.form-section {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 80%;
  max-width: 500px;
}

.product-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-form input, .product-form select, .product-form textarea, .product-form button {
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.product-form button {
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.product-form button:hover {
  background-color: #0056b3;
}

</style>


