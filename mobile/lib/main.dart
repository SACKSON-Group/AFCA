import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const AfcaApp());
}

class AfcaApp extends StatelessWidget {
  const AfcaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AFCA Mobile',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blue),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _nameCtrl = TextEditingController();
  final _providerCtrl = TextEditingController(text: 'doc-001');
  final _reasonCtrl = TextEditingController();

  List<dynamic> _providers = [];
  String _status = '';

  // Android emulator: 10.0.2.2, iOS simulator: localhost
  final String _baseUrl = 'http://10.0.2.2:8000';

  Future<void> loadProviders() async {
    final res = await http.get(Uri.parse('$_baseUrl/api/providers'));
    if (res.statusCode != 200) {
      setState(() => _status = 'Failed to load providers');
      return;
    }

    final data = jsonDecode(res.body) as Map<String, dynamic>;
    setState(() {
      _providers = data['items'] as List<dynamic>;
      _status = 'Loaded ${_providers.length} providers';
    });
  }

  Future<void> bookAppointment() async {
    final payload = {
      'patient_name': _nameCtrl.text.trim(),
      'provider_id': _providerCtrl.text.trim(),
      'scheduled_at': DateTime.now().toIso8601String(),
      'mode': 'audio',
      'reason': _reasonCtrl.text.trim(),
    };

    final res = await http.post(
      Uri.parse('$_baseUrl/api/appointments'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload),
    );

    if (res.statusCode != 201) {
      setState(() => _status = 'Booking failed: ${res.body}');
      return;
    }

    final data = jsonDecode(res.body) as Map<String, dynamic>;
    setState(() => _status = 'Appointment created: ${data['id']}');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AFCA Mobile')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            ElevatedButton(
              onPressed: loadProviders,
              child: const Text('Load Providers'),
            ),
            const SizedBox(height: 8),
            ..._providers.map((p) => ListTile(
                  title: Text(p['name']),
                  subtitle: Text('${p['specialty']} • ${p['country']}'),
                )),
            const Divider(),
            TextField(
              controller: _nameCtrl,
              decoration: const InputDecoration(labelText: 'Patient name'),
            ),
            TextField(
              controller: _providerCtrl,
              decoration: const InputDecoration(labelText: 'Provider ID'),
            ),
            TextField(
              controller: _reasonCtrl,
              decoration: const InputDecoration(labelText: 'Reason'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: bookAppointment,
              child: const Text('Book Appointment'),
            ),
            const SizedBox(height: 12),
            Text(_status),
          ],
        ),
      ),
    );
  }
}
