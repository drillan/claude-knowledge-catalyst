---
title: "React Component Best Practices"
project: "Frontend-Team"
tags: ["code", "react", "frontend"]
category: "code"
status: "production"
author: "Frontend Team Lead"
---

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
