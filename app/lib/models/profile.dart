class Profile {
  Profile({
    required this.id,
    required this.createdAt,
  });

  /// User ID of the profile
  final String id;


  /// Date and time when the profile was created
  final DateTime createdAt;

  Profile.fromMap(Map<String, dynamic> map)
      : id = map['id'],
        createdAt = DateTime.parse(map['created_at']);
}