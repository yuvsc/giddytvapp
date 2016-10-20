import java.util.ArrayList;

public class Update {

	private String title, description; 
	private ArrayList<String> images;
	
	public String getTitle (){
		return title;
	}
	public String getDes () {
		return description;
	}
	public String getImage (int i){
		return images.get(i);
	}
	public void setTitle (String a){
		title = a;
	}
	public void setDes (String d){
		description = d;
	}
	public void setImage (String username, String code){
		images.add("https://firstbuild-stg.herokuapp.com/v1/users/" + username + "/uploads/" + code);
	}

}
