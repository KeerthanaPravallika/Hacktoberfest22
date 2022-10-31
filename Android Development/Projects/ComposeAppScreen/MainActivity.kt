import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Column
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.sp
import com.example.week1compose.ui.theme.Week1ComposeTheme

/* 
   This is code for a simple UI screen made using Jetpack Compose
   Create a new project of type "Empty Compose Activity" in your android studio
   Modify the contents of your ./app/src/main/java/com/example/<projectname>/MainActivity.kt (copy paste from here)
   Add a new image of jetpack compose using resource manager and name it "logocompose.png"
   After following these you should be able to see the output in your testing device!
*/

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Week1ComposeTheme {
                // A surface container using the 'background' color from the theme
                Surface(color = MaterialTheme.colors.background) {
                    ComposeGreeting("Sarika")
                }
            }
        }
    }
}

@Composable
fun ComposeGreeting(name: String) {
    Column (horizontalAlignment = Alignment.CenterHorizontally) {

        Image(painter = painterResource(id = R.drawable.logocompose), contentDescription = null)
        Text(text = name, color = Color(56, 112, 179, 255), fontSize = 24.sp)
        Text(text = "❤️", fontSize = 90.sp)
        Text(text = "Jetpack Compose", color = Color(8, 48, 66, 255), fontSize = 24.sp)
    }

}

@Preview(showBackground = true)
@Composable
fun Preview() {
    Week1ComposeTheme {
        // You can change the name parameter to display your own name!
        ComposeGreeting("Soumya")
    }
}
