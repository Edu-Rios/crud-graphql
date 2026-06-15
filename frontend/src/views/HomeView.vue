<script setup lang="ts">
import { ref } from 'vue'
import { useQuery, useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

// --- QUERIES Y MUTATIONS ---
// Strawberry convierte automáticamente "get_categories" de Python a "getCategories" en GraphQL
const GET_CATEGORIES = gql`
  query { getCategories { id name } }
`
const GET_PRODUCTS = gql`
  query { getProducts { id name stock price category { name } } }
`
const CREATE_PRODUCT = gql`
  mutation CreateProduct($name: String!, $price: Float!, $stock: Int!, $categoryId: Int!) {
    createProduct(name: $name, price: $price, stock: $stock, categoryId: $categoryId) { id name stock }
  }
`
const DELETE_PRODUCT = gql`
  mutation DeleteProduct($productId: Int!) { deleteProduct(productId: $productId) }
`
const REGISTER_SALE = gql`
  mutation RegisterSale($productId: Int!, $quantity: Int!) {
    registerSale(productId: $productId, quantity: $quantity) { id stock }
  }
`

// --- LÓGICA Y ESTADO ---
const { result: categoriesResult } = useQuery(GET_CATEGORIES)
const { result, loading, error } = useQuery(GET_PRODUCTS)

// Estado del formulario
const newProduct = ref({ name: '', price: 0, stock: 0, categoryId: null as number | null })

const { mutate: createProduct } = useMutation(CREATE_PRODUCT, {
  refetchQueries: [{ query: GET_PRODUCTS }]
})

const { mutate: deleteProduct } = useMutation(DELETE_PRODUCT, {
  refetchQueries: [{ query: GET_PRODUCTS }]
})

const { mutate: registerSale } = useMutation(REGISTER_SALE)

// --- MANEJADORES DE ACCIONES ---
const handleCreate = () => {
  if (!newProduct.value.name || newProduct.value.price <= 0 || !newProduct.value.categoryId) {
    return alert('Por favor, llena todos los campos y selecciona una categoría.')
  }
  createProduct(newProduct.value)
  // Limpiar el formulario después de guardar
  newProduct.value = { name: '', price: 0, stock: 0, categoryId: null }
}

const handleDelete = (id: number) => {
  if (confirm('¿Deseas eliminar este registro de forma permanente?')) {
    deleteProduct({ productId: id })
  }
}

const handleSell = (id: number) => {
  registerSale({ productId: id, quantity: 1 })
}
</script>

<template>
  <div class="dashboard">
    <header class="main-header">
      <div class="title-section">
        <h1>Gestión de Inventario</h1>
      </div>
    </header>

    <section class="card creation-card">
      <div class="card-header">
        <div class="icon-circle">＋</div>
        <h3>Registrar Nuevo Producto</h3>
      </div>
      
      <div class="form-grid">
        <div class="input-group">
          <label>Nombre del Producto</label>
          <input v-model="newProduct.name" placeholder="Ej. Monitor Studio Display" />
        </div>

        <div class="input-group">
          <label>Categoría</label>
          <select v-model="newProduct.categoryId" class="custom-select">
            <option :value="null" disabled>Selecciona una...</option>
            <option v-for="cat in categoriesResult?.getCategories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <div class="input-group">
          <label>Precio Unitario ($)</label>
          <input v-model.number="newProduct.price" type="number" step="0.01" placeholder="0.00" />
        </div>

        <div class="input-group">
          <label>Stock Inicial</label>
          <input v-model.number="newProduct.stock" type="number" placeholder="0" />
        </div>

        <div class="input-group actions">
          <button @click="handleCreate" class="btn btn-save">
            Guardar Producto
          </button>
        </div>
      </div>
    </section>

    <section class="card table-card">
      <div v-if="loading" class="loader">
        <div class="spinner"></div>
        <p>Sincronizando con la nube...</p>
      </div>

      <div v-else-if="error" class="status-msg error">
        ❌ Error de conexión: {{ error.message }}
      </div>

      <div v-else class="table-wrapper">
        <table v-if="result && result.getProducts.length">
          <thead>
            <tr>
              <th>ID</th>
              <th>Información del Producto</th>
              <th>Disponibilidad</th>
              <th>Precio</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in result.getProducts" :key="product.id">
              <td class="text-muted">#{{ product.id }}</td>
              <td>
                <div class="product-info">
                  <span class="p-name">{{ product.name }}</span>
                  <span class="p-cat">{{ product.category ? product.category.name : 'General' }}</span>
                </div>
              </td>
              <td>
                <div class="stock-badge" :class="product.stock < 10 ? 'low' : 'ok'">
                  {{ product.stock }} unidades
                </div>
              </td>
              <td class="p-price">${{ product.price.toLocaleString() }}</td>
              <td>
                <div class="button-group">
                  <button @click="handleSell(product.id)" :disabled="product.stock <= 0" class="btn-icon btn-sell" title="Vender 1">
                    💸 Vender
                  </button>
                  <button @click="handleDelete(product.id)" class="btn-icon btn-delete" title="Eliminar">
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div v-else class="empty-state">
          <p>No hay productos registrados actualmente.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Estilos Base - Dark Theme */
.dashboard {
  color: #e2e8f0;
  min-height: 100vh;
  padding-bottom: 20px;
}

.main-header {
  margin-bottom: 30px;
}

.badge {
  background: #1e293b;
  color: #818cf8;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  border: 1px solid #334155;
}

h1 {
  font-size: 2.2rem;
  margin-top: 10px;
  background: linear-gradient(to right, #8a8a8a, #454b52);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Tarjetas */
.card {
  background: #111827;
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.icon-circle {
  background: #312e81;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #818cf8;
  font-weight: bold;
}

/* Formulario */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
  align-items: flex-end;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 0.85rem;
  color: #94a3b8;
  font-weight: 500;
}

input, .custom-select {
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 8px;
  padding: 12px;
  color: #f3f4f6;
  transition: all 0.3s;
  outline: none;
}

input:focus, .custom-select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.custom-select {
  cursor: pointer;
  appearance: auto;
}

/* Botones */
.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: 0.3s;
  width: 100%;
}

.btn-save {
  background: #6366f1;
  color: white;
}

.btn-save:hover {
  background: #4f46e5;
  transform: translateY(-2px);
}

/* Tabla Estilo Elegante */
.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 8px;
}

th {
  text-align: left;
  padding: 12px;
  color: #64748b;
  font-size: 0.85rem;
  text-transform: uppercase;
}

td {
  padding: 16px 12px;
  background: #1f2937;
}

td:first-child { border-radius: 12px 0 0 12px; }
td:last-child { border-radius: 0 12px 12px 0; }

.product-info {
  display: flex;
  flex-direction: column;
}

.p-name {
  font-weight: 600;
  color: #f8fafc;
}

.p-cat {
  font-size: 0.75rem;
  color: #64748b;
}

.stock-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
}

.stock-badge.ok { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.stock-badge.low { background: rgba(239, 68, 68, 0.1); color: #ef4444; }

.p-price {
  font-weight: bold;
  color: #f8fafc;
}

/* Botones de Acción */
.button-group {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-icon {
  border: none;
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  transition: 0.2s;
}

.btn-sell {
  background: #064e3b;
  color: #34d399;
}

.btn-sell:hover:not(:disabled) { background: #065f46; }

.btn-delete {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.btn-delete:hover { background: rgba(239, 68, 68, 0.2); }

.btn-icon:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Estados Vacíos y Carga */
.loader {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}

.spinner {
  border: 3px solid #1f2937;
  border-top: 3px solid #6366f1;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}

.text-right { text-align: right; }
.text-muted { color: #4b5563; }
</style>