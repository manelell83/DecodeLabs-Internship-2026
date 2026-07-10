from core.password_analyzer import PasswordAnalyzer


if __name__ == "__main__":
    analyzer = PasswordAnalyzer()
    password = input("Enter a password to analyze: ")
    result = analyzer.analyze(password)
    print(f"Score: {result.score}/100")
    print(f"Level: {result.level}")
    print(f"Entropy: {result.entropy:.1f} bits")
    print("Checklist:")
    for key, value in result.checklist.items():
        print(f"- {key}: {'passed' if value else 'failed'}")
    print("Suggestions:")
    for suggestion in result.suggestions:
        print(f"- {suggestion}")
