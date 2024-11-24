# yFinance Crawler

- **First run**: Update the `ENTRYPOINT` to include the migration scripts:  
  `ENTRYPOINT ["python", "./migrations/create_table_stock_data_and_users.py", "./migrations/test_user_data_seeder.py", "crawler.py"]`.
- **Subsequent runs**: Use the default `ENTRYPOINT ["python", "./crawler.py"]` to skip migrations.  
  Rebuild the container when switching `ENTRYPOINT`.
