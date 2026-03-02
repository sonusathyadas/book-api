using System.ComponentModel.DataAnnotations;

namespace BookApi.Models;

public class Book
{
    public int Id { get; set; }

    [Required]
    [MaxLength(200)]
    public string Title { get; set; } = string.Empty;

    [Required]
    [MaxLength(100)]
    public string Author { get; set; } = string.Empty;

    [Range(1, 9999)]
    public int PublishedYear { get; set; }

    [Required]
    [MaxLength(50)]
    public string Genre { get; set; } = string.Empty;
}
