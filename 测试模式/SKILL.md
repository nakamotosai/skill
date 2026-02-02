---
description: 测试生成和运行指令。为代码创建并执行测试。
---

# /test - 测试生成与执行

$ARGUMENTS

---

## 目的

此指令用于生成测试、运行现有测试或检查测试覆盖率。

---

## 子指令

```
/test                - 运行所有测试
/test [file/feature] - 为特定目标生成测试
/test coverage       - 显示测试覆盖率报告
/test watch          - 以监视模式运行测试
```

---

## 行为

### 生成测试

当要求测试文件或功能时：

1. **分析代码**
   - 识别函数和方法
   - 发现边缘情况
   - 检测需模拟的依赖项

2. **生成测试用例**
   - 快乐路径 (Happy path) 测试
   - 错误情况
   - 边缘情况
   - 集成测试 (如果需要)

3. **编写测试**
   - 使用项目的测试框架 (Jest, Vitest 等)
   - 遵循现有的测试模式
   - 模拟外部依赖

---

## 输出格式

### 用于测试生成

```markdown
## 🧪 测试: [目标]

### 测试计划
| 测试用例 | 类型 | 覆盖范围 |
|-----------|------|----------|
| Should create user | Unit | Happy path |
| Should reject invalid email | Unit | Validation |
| Should handle db error | Unit | Error case |

### 生成的测试

`tests/[file].test.ts`

[Code block with tests]

---

运行: `npm test`
```

### 用于测试执行

```
🧪 Running tests...

✅ auth.test.ts (5 passed)
✅ user.test.ts (8 passed)
❌ order.test.ts (2 passed, 1 failed)

Failed:
  ✗ should calculate total with discount
    Expected: 90
    Received: 100

Total: 15 tests (14 passed, 1 failed)
```

---

## 示例

```
/test src/services/auth.service.ts
/test user registration flow
/test coverage
/test fix failed tests
```

---

## 测试模式

### 单元测试结构

```typescript
describe('AuthService', () => {
  describe('login', () => {
    it('should return token for valid credentials', async () => {
      // Arrange
      const credentials = { email: 'test@test.com', password: 'pass123' };

      // Act
      const result = await authService.login(credentials);

      // Assert
      expect(result.token).toBeDefined();
    });

    it('should throw for invalid password', async () => {
      // Arrange
      const credentials = { email: 'test@test.com', password: 'wrong' };

      // Act & Assert
      await expect(authService.login(credentials)).rejects.toThrow('Invalid credentials');
    });
  });
});
```

---

## 关键原则

- **测试行为而非实现**
- **每个测试一个断言** (在可行的情况下)
- **描述性的测试名称**
- **Arrange-Act-Assert (准备-执行-断言) 模式**
- **模拟外部依赖**
