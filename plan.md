

- [ ] **Расширить тесты.** Сейчас есть только `test/test_user.py`; добавить
  tests для category, store и item: все CRUD-сценарии, 401/403, 404, дубликаты,
  невалидную пагинацию, деактивацию и foreign keys. Проверять response schema,
  отсутствие `ofd_token` в публичных ответах и отсутствие HTTP 500 на
  ожидаемых ошибках. Убрать неиспользуемые импорты и отладочный вывод из
  `test/conftest.py` и `test/test_user.py`.

## После исправлений

- [ ] Запустить `pytest -q`, `alembic upgrade head` на пустой тестовой
  PostgreSQL базе и ручную проверку OpenAPI (`/docs`).
- [ ] Добавить статический анализ (ruff) и проверку типов (mypy/pyright) в CI:
  они сразу выявили бы отсутствующие `await`, опечатку аргумента маршрута и
  несовпадение сигнатуры `get_all_items`.


## Понять

- [ ] **[security.py](src/user/security.py)** почему работает asynnc здесь? 

- [ ] **[sevice.py](src/user/service.py)** line: 31 - 38. 
```python
    async def get_user_by_id(self, user_id: int, return_schema, is_active: bool | None = None) -> ???:
        user = await self.user_dao.get_by_id(user_id, is_active)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user in not found"
            )
        return return_schema.model_validate(user)
```
Нужно сделать возможность поставить правило возвращение результата: `def(a,b, ReturnShemas) -> ReturnShemas` 

- [ ] **не хочу что бы все слилось в кашу по этому админку сделаю отдельно от user и всех роутов** 
- [ ] **ну или полностью разделить вме логики проверок от service** 


-  [ ] **понять lambda функции**
```python
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole, values_callable=lambda obj: [e.value for e in obj]), 
        default=UserRole.CUSTOMER, 
        server_default="customer"
    )
```