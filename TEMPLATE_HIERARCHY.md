# Template Hierarchy Structure

```
rent/templates/rent/
│
├── base.html (DEPRECATED - no longer used)
│
├── base_public.html (NEW - For unauthenticated customers)
│   ├── Style: public-body class
│   ├── Layout: Full-width, no sidebar
│   ├── Navbar: Login/Logout button
│   ├── Content: Full-width with footer
│   └── Used by:
│       ├── customers/room_list.html
│       └── customers/room_detail.html
│
├── base_authenticated.html (NEW - Base for all authenticated users)
│   ├── Style: dashboard-body class
│   ├── Layout: Sidebar (240px) + Main content
│   ├── Blocks:
│   │   ├── sidebar_links (to be overridden)
│   │   ├── search_box (to be overridden)
│   │   └── content
│   ├── Features:
│   │   ├── Fixed Sidebar
│   │   ├── Top Header with user info
│   │   └── Responsive design
│   │
│   ├── base_owner.html (NEW - For Owner Dashboard)
│   │   ├── Extends: base_authenticated.html
│   │   ├── Sidebar Links:
│   │   │   ├── Dashboard
│   │   │   ├── Rooms (list)
│   │   │   ├── Add Room
│   │   │   ├── Management
│   │   │   ├── Tenants
│   │   │   └── Profile
│   │   ├── Search Box: Room search
│   │   └── Used by:
│   │       ├── owners/dashboard.html
│   │       ├── owners/room_list.html
│   │       ├── owners/add_room.html
│   │       ├── owners/edit_room.html
│   │       ├── owners/room_detail.html
│   │       ├── owners/tenant_list.html
│   │       ├── owners/tenant_detail.html
│   │       ├── owners/add_tenant.html
│   │       ├── owners/assign_tenant.html
│   │       ├── owners/management.html
│   │       ├── owners/profile.html
│   │       └── owners/bookings_list.html
│   │
│   └── base_tenant.html (NEW - For Tenant Dashboard)
│       ├── Extends: base_authenticated.html
│       ├── Sidebar Links:
│       │   ├── Dashboard
│       │   ├── Profile
│       │   ├── Payments
│       │   └── Support
│       ├── Search Box: Simple header
│       └── Used by:
│           ├── tenants/dashboard.html
│           └── tenants/profile.html
```

## CSS Layout Classes

### Public Pages (customers/room_list, customers/room_detail)
```css
body.public-body {
    padding-top: 70px;
    display: block;
}

.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 70px;
    background-color: white;
    z-index: 1000;
}

.main-public-content {
    width: 100%;
    margin-left: 0;
    min-height: calc(100vh - 140px);
}
```

### Dashboard Pages (owners/*, tenants/*)
```css
body.dashboard-body {
    margin: 0;
    display: flex;
    background-color: #f8faff;
}

.sidebar {
    width: 240px;
    background: white;
    height: 100vh;
    position: fixed;
}

.main-content {
    margin-left: 240px;
    width: calc(100% - 240px);
}
```

## Navigation Bar Structure

### Public Pages (base_public.html)
```
┌─────────────────────────────────────────────────────┐
│ Logo  Browse Rooms  [Login Button]                  │
│ Home                                                │
└─────────────────────────────────────────────────────┘
```

### Dashboard Pages (base_authenticated.html)
```
┌──────────────┬─────────────────────────────────────┐
│              │ [Search Box]  [🔔]  [User Name]    │
│   SIDEBAR    ├─────────────────────────────────────┤
│              │                                     │
│  Dashboard   │  MAIN CONTENT AREA                  │
│  Rooms       │                                     │
│  Add Room    │                                     │
│  Management  │                                     │
│  Tenants     │                                     │
│  Profile     │                                     │
│              │                                     │
│  Settings    │                                     │
│  Logout      │                                     │
│              │                                     │
└──────────────┴─────────────────────────────────────┘
```

## Flow Chart - User Journey

```
Visit Website
    ↓
[/customers/] (room_list) → base_public.html
    ├─ No Sidebar
    ├─ Login Button visible
    ├─ Full-width room grid
    └─ Click Login
        ↓
    [Login Page] → Authenticate
        ├─ If Owner
        │  └─ Redirect to [/owners/dashboard]
        │     └─ base_owner.html (extends base_authenticated)
        │        ├─ Sidebar with owner links
        │        ├─ Owner-specific search
        │        └─ Dashboard stats
        │
        ├─ If Tenant
        │  └─ Redirect to [/tenants/dashboard]
        │     └─ base_tenant.html (extends base_authenticated)
        │        ├─ Sidebar with tenant links
        │        ├─ Tenant-specific header
        │        └─ Payment status
        │
        └─ If Customer (Generic)
           └─ Redirect to [/customers/] (room_list)
              └─ base_public.html (no changes to layout)
```

## Summary

| Aspect | Public Pages | Owner Dashboard | Tenant Dashboard |
|--------|-------------|-----------------|-----------------|
| **Base Template** | base_public.html | base_owner.html | base_tenant.html |
| **Layout Type** | Full-width | Sidebar + Main | Sidebar + Main |
| **Sidebar** | ❌ None | ✅ Owner navigation | ✅ Tenant navigation |
| **Top Navbar** | ✅ Login/Logout | ✅ Search + User | ✅ Simple header |
| **CSS Class** | public-body | dashboard-body | dashboard-body |
| **Sidebar Width** | - | 240px | 240px |
| **Main Content** | 100% width | calc(100% - 240px) | calc(100% - 240px) |
