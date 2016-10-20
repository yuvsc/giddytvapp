import java.util.ArrayList;

public class Project {

	private String title, description, image;
	private ArrayList<User> team;
	private ArrayList<Update> updates;
	
	public String getTitle() {
		return title;
	}
	public String getDetail() {
		return description;
	}
	public String getImage() {
		return image;
	}
	public User getTeamMember(int i){
		return team.get(i);
	}
	public Update getUpdate(int i){
		return updates.get(i);
	}
	
	public void setTitle (String a){
		title = a;
	}
	public void setDetail (String a){
		description = a;
	}
	public void setImage(String URL){
		image = URL;
	}
	public void addTeamMember (User user){
		team.add(user);
	}
	public void addUpdate (Update update){
		updates.add(update);
	}

}
