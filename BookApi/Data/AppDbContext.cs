using BookApi.Models;
using Microsoft.EntityFrameworkCore;

namespace BookApi.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    // SECURITY: Only use LINQ and parameterized queries. Avoid raw SQL or string concatenation for queries.

    public DbSet<Book> Books { get; set; }
}
