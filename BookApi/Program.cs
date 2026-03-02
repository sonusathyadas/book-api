using BookApi.Data;
using BookApi.Repositories;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
// Add Swagger only in development
if (builder.Environment.IsDevelopment())
{
    builder.Services.AddEndpointsApiExplorer();
    builder.Services.AddSwaggerGen();
}


// Add CORS policy - restrict to trusted origins
builder.Services.AddCors(options =>
{
    options.AddPolicy("TrustedOrigins", policy =>
    {
        policy.WithOrigins("https://yourtrustedclient.com") // TODO: Replace with actual trusted origins
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

builder.Services.AddControllers();

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection") ?? "Data Source=books.db"));

builder.Services.AddScoped<IBookRepository, BookRepository>();

var app = builder.Build();
// Use Swagger only in development
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Global error handler to avoid stack trace exposure
app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        context.Response.StatusCode = 500;
        context.Response.ContentType = "application/json";
        await context.Response.WriteAsync("{\"message\":\"An unexpected error occurred.\"}");
    });
});

// Ensure the database is created.
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

// Configure the HTTP request pipeline.
app.UseHttpsRedirection();

// Use CORS policy
app.UseCors("TrustedOrigins");

app.MapControllers();

app.Run();
