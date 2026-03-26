# Saftehnika Frontend

Vue 3 + TypeScript + Vite application for sensor data visualization.

## Architecture

This application follows Vue 3 best practices with:

- **TypeScript** for type safety
- **Composition API** for reactive logic
- **Provide/Inject** for global state management
- **Path aliases** (`@/`) for clean imports
- **Centralized API client** for all HTTP requests

## Project Structure

```
src/
├── components/          # Reusable Vue components
│   └── MeasurementsTable.vue  # Measurements display & filtering
├── composables/         # Reusable composition functions
│   └── useMeasurements.ts     # Measurements data logic
├── stores/              # Reactive global state modules
│   └── structure.ts    # Global structure data (sensors & metrics)
├── config/              # Configuration files
│   └── env.ts          # Environment variables
├── services/            # API clients and external services
│   └── api.ts          # HTTP client
├── types/               # TypeScript type definitions
│   ├── measurement.ts  # Measurement & filter types
│   └── structure.ts    # Structure data types
├── App.vue             # Root component
└── main.ts             # Application entry point
```

## Environment Variables

Environment variables are managed through Docker and must be prefixed with `VITE_` to be exposed to the client.

**Available Variables:**
- `VITE_API_URL` - API base URL (from Docker .env)

## Global State: Structure Data

The application loads sensor types and metrics data once on mount. Since this data is static and doesn't change, it's implemented as a simple reactive module (not a composable or full store).

### Load Once (App.vue)

```typescript
import { loadStructure } from '@/stores/structure'

onMounted(() => {
  loadStructure()
})
```

### Access Anywhere (Any component)

```typescript
import { structure, getSensorTypeById, getMetricById } from '@/stores/structure'

// Direct reactive access
const sensorTypes = structure.value?.sensor_types
const metrics = structure.value?.metrics

// Helper methods
const sensor = getSensorTypeById(1)
const metric = getMetricById(1)
```

**Why not a composable?** Since structure data loads once and never changes, a simple reactive module is more appropriate than provide/inject or a full state management solution.

## Dynamic Data: Measurements

Measurements data changes based on filters, so it uses a **composable** for reusable stateful logic.

### Using the Measurements Composable

```typescript
import { useMeasurements } from '@/composables/useMeasurements'

const measurements = useMeasurements()

// Fetch with filters (replaces previous data)
await measurements.fetch({ type_id: '18' })

// Access data
const sensors = measurements.data.value
const isLoading = measurements.isLoading.value

// Refresh with current filters
await measurements.refresh()

// Clear all data
measurements.clear()
```

### Why a Composable for Measurements?

| Aspect | Measurements | Pattern Choice |
|--------|-------------|----------------|
| **Changes?** | Yes (on filter) | Composable ✅ |
| **Stateful?** | Yes (loading, error) | Composable ✅ |
| **Reusable?** | Potentially | Composable ✅ |
| **Previous data needed?** | No | Simple replacement ✅ |

## API Client

All API calls go through the centralized `apiClient` service:

```typescript
import { apiClient } from '@/services/api'

// Get structure data
const structure = await apiClient.getStructure()

// Get measurements
const measurements = await apiClient.getMeasurements({ 
  sensor_id: '123' 
})
```

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Docker

```bash
# Build and start all services
docker-compose up --build

# Access the app
open http://localhost:3002
```

## Best Practices Implemented

1. **Single Responsibility** - Each file has a clear purpose
2. **Type Safety** - Full TypeScript coverage
3. **Error Handling** - Proper error boundaries and user feedback
4. **Loading States** - User-friendly loading indicators
5. **Readonly State** - State is read-only outside composables
6. **Path Aliases** - Clean imports with `@/` prefix
7. **Environment Validation** - Runtime checks for required env vars
8. **API Client** - Centralized HTTP logic with error handling
9. **Composition API** - Modern Vue 3 patterns
10. **Component Modularity** - Small, focused components
