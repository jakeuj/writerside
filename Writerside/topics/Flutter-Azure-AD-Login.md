# Flutter Azure AD Login

This Flutter application demonstrates how to implement Azure Active Directory (Azure AD) login using the `aad_oauth` package. It allows users to log in with their Azure AD credentials and displays their profile information.

## Dependencies

```yaml
dependencies:
  aad_oauth: ^1.0.0
```

## Sample Code

```dart
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:aad_oauth/aad_oauth.dart';
import 'package:aad_oauth/model/config.dart';

void main() {
  runApp(const MyApp());
}

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Azure AD Login',
      home: const LoginPage(),
      navigatorKey: navigatorKey,
    );
  }
}

class AuthService {
  static const String tenantId = 'xxxx-xxxx-xxxx-xxxx-xxxx';
  static const String clientId = 'xxxx-xxxx-xxxx-xxxx-xxxx';
  static const String redirectUri = 'http://localhost';
  static const String scope = 'openid profile email';

  static AadOAuth get oauth => AadOAuth(
        Config(
          tenant: tenantId,
          clientId: clientId,
          redirectUri: redirectUri,
          navigatorKey: navigatorKey,
          scope: scope,
        ),
      );
}

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final AadOAuth _oauth = AuthService.oauth;
  bool _isLoading = false;

  Future<void> login() async {
    setState(() => _isLoading = true);
    try {
      await _oauth.login();
      await _oauth.getAccessToken(); // 可省略但保留
      final idToken = await _oauth.getIdToken();

      if (!mounted || idToken == null) return;

      final userInfo = _parseIdToken(idToken);
      if (!mounted) return;

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ProfilePage(userInfo: userInfo),
        ),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('登入失敗: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  Map<String, dynamic> _parseIdToken(String token) {
    final payload = token.split('.')[1];
    final normalized = base64Url.normalize(payload);
    final decoded = utf8.decode(base64Url.decode(normalized));
    return json.decode(decoded);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Azure AD 登入')),
      body: Center(
        child: _isLoading
            ? const CircularProgressIndicator()
            : ElevatedButton(
                onPressed: login,
                child: const Text('使用 Azure AD 登入'),
              ),
      ),
    );
  }
}

class ProfilePage extends StatelessWidget {
  final Map<String, dynamic> userInfo;

  const ProfilePage({super.key, required this.userInfo});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('使用者資訊'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await AuthService.oauth.logout();
              if (context.mounted) Navigator.pop(context);
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: CircleAvatar(
                radius: 50,
                backgroundColor: Colors.blue.shade100,
                child: Text(
                  _getInitials(),
                  style: TextStyle(fontSize: 40, color: Colors.blue.shade800),
                ),
              ),
            ),
            const SizedBox(height: 20),
            _buildInfoCard('姓名', userInfo['name'] ?? '未提供'),
            _buildInfoCard(
              '信箱',
              userInfo['email'] ?? userInfo['preferred_username'] ?? '未提供',
            ),
            _buildInfoCard(
              '使用者 ID',
              userInfo['oid'] ?? userInfo['sub'] ?? '未提供',
            ),
            if (userInfo['roles'] != null)
              _buildInfoCard(
                '角色',
                (userInfo['roles'] as List<dynamic>).join(', '),
              ),
          ],
        ),
      ),
    );
  }

  String _getInitials() {
    final name = userInfo['name'] ?? userInfo['preferred_username'] ?? '';
    final parts = (name as String).split(' ');
    return parts.length >= 2
        ? '${parts.first[0]}${parts.last[0]}'.toUpperCase()
        : name.isNotEmpty
            ? name[0].toUpperCase()
            : '?';
  }

  Widget _buildInfoCard(String label, String value) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(fontSize: 14, color: Colors.grey)),
            const SizedBox(height: 4),
            Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}
```