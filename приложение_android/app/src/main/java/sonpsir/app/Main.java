package sonpsir.app;
import android.app.Activity;import android.os.Bundle;import android.webkit.WebView;
public class Main extends Activity{protected void onCreate(Bundle s){super.onCreate(s);WebView w=new WebView(this);w.getSettings().setJavaScriptEnabled(true);w.loadUrl("http://10.0.2.2:8080");setContentView(w);}}