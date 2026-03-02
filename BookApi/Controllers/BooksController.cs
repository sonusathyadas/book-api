using BookApi.Models;
using BookApi.Repositories;
using Microsoft.AspNetCore.Mvc;

namespace BookApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class BooksController : ControllerBase
{
    private readonly IBookRepository _repository;
    private readonly ILogger<BooksController> _logger;

    public BooksController(IBookRepository repository, ILogger<BooksController> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    // GET /api/books
    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        try
        {
            var books = await _repository.GetAllAsync();
            return Ok(books);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving all books.");
            return StatusCode(500, new { message = "An error occurred while retrieving books." });
        }
    }

    // GET /api/books/{id}
    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
        try
        {
            var book = await _repository.GetByIdAsync(id);
            if (book is null)
                return NotFound(new { message = $"Book with id {id} not found." });

            return Ok(book);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving book with id {Id}.", id);
            return StatusCode(500, new { message = "An error occurred while retrieving the book." });
        }
    }

    // POST /api/books
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] Book book)
    {
        try
        {
            var created = await _repository.AddAsync(book);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating book.");
            return StatusCode(500, new { message = "An error occurred while creating the book." });
        }
    }

    // PUT /api/books/{id}
    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, [FromBody] Book book)
    {
        try
        {
            var updated = await _repository.UpdateAsync(id, book);
            if (updated is null)
                return NotFound(new { message = $"Book with id {id} not found." });

            return Ok(updated);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating book with id {Id}.", id);
            return StatusCode(500, new { message = "An error occurred while updating the book." });
        }
    }

    // DELETE /api/books/{id}
    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        try
        {
            var deleted = await _repository.DeleteAsync(id);
            if (!deleted)
                return NotFound(new { message = $"Book with id {id} not found." });

            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting book with id {Id}.", id);
            return StatusCode(500, new { message = "An error occurred while deleting the book." });
        }
    }
}
