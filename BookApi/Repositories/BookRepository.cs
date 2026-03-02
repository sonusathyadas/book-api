using BookApi.Data;
using BookApi.Models;
using Microsoft.EntityFrameworkCore;

namespace BookApi.Repositories;

public class BookRepository : IBookRepository
{
    private readonly AppDbContext _context;

    public BookRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Book>> GetAllAsync()
    {
        return await _context.Books.ToListAsync();
    }

    public async Task<Book?> GetByIdAsync(int id)
    {
        return await _context.Books.FindAsync(id);
    }

    public async Task<Book> AddAsync(Book book)
    {
        _context.Books.Add(book);
        await _context.SaveChangesAsync();
        return book;
    }

    public async Task<Book?> UpdateAsync(int id, Book book)
    {
        var existing = await _context.Books.FindAsync(id);
        if (existing is null)
            return null;

        existing.Title = book.Title;
        existing.Author = book.Author;
        existing.PublishedYear = book.PublishedYear;
        existing.Genre = book.Genre;

        await _context.SaveChangesAsync();
        return existing;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var existing = await _context.Books.FindAsync(id);
        if (existing is null)
            return false;

        _context.Books.Remove(existing);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<IEnumerable<Book>> GetByAuthorAsync(string author, int page, int pageSize)
    {
        if (string.IsNullOrWhiteSpace(author))
            return new List<Book>();
        var term = author.Trim();
        return await _context.Books
            .Where(b => EF.Functions.Like(b.Author, "%" + term + "%"))
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();
    }
}
