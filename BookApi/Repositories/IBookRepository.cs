using BookApi.Models;

namespace BookApi.Repositories;

public interface IBookRepository
{
    Task<IEnumerable<Book>> GetAllAsync();
    Task<Book?> GetByIdAsync(int id);
    Task<Book> AddAsync(Book book);
    Task<Book?> UpdateAsync(int id, Book book);
    Task<bool> DeleteAsync(int id);
    Task<IEnumerable<Book>> GetByAuthorAsync(string author, int page, int pageSize);
}
