import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class PasswordStrengthAssessor {
    public static String assessPasswordStrength(String password) {
        // Check password length
        if (password.length() < 8) {
            return "Weak - Password is too short";
        }

        // Check for common password patterns
        String[] commonPatterns = {
            "(?i)password",
            "(?i)123456",
            "(?i)qwerty",
            "(?i)abcdef",
            "(?i)p@ssw0rd"
        };
        for (String pattern : commonPatterns) {
            Pattern compiledPattern = Pattern.compile(pattern);
            Matcher matcher = compiledPattern.matcher(password);
            if (matcher.find()) {
                return "Weak - Password is too common";
            }
        }

        // Check for complexity
        if (!Pattern.compile("[a-z]").matcher(password).find()) {
            return "Weak - Password must contain at least one lowercase letter";
        }
        if (!Pattern.compile("[A-Z]").matcher(password).find()) {
            return "Weak - Password must contain at least one uppercase letter";
        }
        if (!Pattern.compile("[0-9]").matcher(password).find()) {
            return "Weak - Password must contain at least one digit";
        }
        if (!Pattern.compile("[^A-Za-z0-9]").matcher(password).find()) {
            return "Weak - Password must contain at least one special character";
        }

        // If all checks pass, the password is considered strong
        return "Strong";
    }

    public static void main(String[] args) {
        String password = "MyStrongPassword!";
        String result = assessPasswordStrength(password);
        System.out.println(result);
    }
}

