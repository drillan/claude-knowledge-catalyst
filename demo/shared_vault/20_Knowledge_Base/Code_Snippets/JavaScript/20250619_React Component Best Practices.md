---
author: Frontend Team Lead
category: code
created: '2025-06-19T00:47:32.812939'
project: Frontend-Team
status: production
tags:
- code
- frontend
- javascript
- react
title: React Component Best Practices
updated: '2025-06-19T00:47:32.812945'
version: '1.0'
---

**Tags:** #code #frontend #javascript #react

# React Component Best Practices

## Component Structure
```jsx
// ✅ Good: Functional component with hooks
const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  
  if (loading) return <Spinner />;
  if (!user) return <ErrorMessage />;
  
  return <div className="user-profile">{user.name}</div>;
};
```

## Performance Tips
- Use React.memo for expensive components
- Optimize re-renders with useMemo and useCallback
- Split large components into smaller ones